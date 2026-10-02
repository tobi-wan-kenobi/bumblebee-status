import io
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest import mock
import urllib.error

import pytest

import core.config
import core.module
import modules.contrib.livetennis as livetennis


def match(match_id=1, score=None):
    return {
        "id": match_id,
        "status": "live",
        "players": {"p1": {"name": "First"}, "p2": {"name": "Second"}},
        "score": score,
    }


def module(*parameters):
    arguments = ["-p"] + list(parameters) if parameters else []
    return core.module.load("livetennis", core.config.Config(arguments))


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("LIVETENNIS_API_KEY", "unit-test-key")
    clock = mock.Mock(return_value=10000)
    monkeypatch.setattr(livetennis.time, "time", clock)
    opener = mock.Mock()
    opener.open.side_effect = lambda *args, **kwargs: io.StringIO(
        json.dumps({"data": [match()]})
    )
    monkeypatch.setattr(
        livetennis.urllib.request, "build_opener", mock.Mock(return_value=opener)
    )
    return opener, clock


def text(mod):
    mod.update()
    return mod.widgets()[0].full_text()


def test_missing_key_makes_no_request(client, monkeypatch):
    monkeypatch.delenv("LIVETENNIS_API_KEY")
    assert text(module()) == "Tennis: missing API key"
    client[0].open.assert_not_called()


def test_request_uses_free_endpoint_and_header(client, tmp_path):
    assert text(module()) == "Tennis: First v Second (score unavailable)"
    request = client[0].open.call_args[0][0]
    assert request.full_url == livetennis.URL
    assert request.get_header("X-api-key") == "unit-test-key"
    assert client[0].open.call_args[1] == {"timeout": 10}
    for path in tmp_path.rglob("*"):
        if path.is_file():
            assert path.stat().st_mode & 0o777 == 0o600
            assert "unit-test-key" not in path.read_text()
            assert "unit-test-key" not in path.name


def test_aliases_and_restarts_share_request_floor(client):
    opener, clock = client
    first = module("livetennis.interval=0.1")
    assert text(first).startswith("Tennis: First")
    for now in (10000, 10001, 10899, 9999):
        clock.return_value = now
        second = core.module.load(
            "livetennis:second", core.config.Config(["-p", "second.interval=0.1"])
        )
        assert text(second) == first.widgets()[0].full_text()
        assert text(module()) == first.widgets()[0].full_text()
    assert opener.open.call_count == 1
    clock.return_value = 10900
    text(first)
    assert opener.open.call_count == 2


@pytest.mark.parametrize(
    "error",
    [
        urllib.error.URLError("offline"),
        ValueError("bad JSON"),
        urllib.error.HTTPError(livetennis.URL, 429, "limited", {}, None),
        urllib.error.HTTPError(livetennis.URL, 401, "invalid", {}, None),
    ],
    ids=["offline", "bad-json", "rate-limit", "invalid-key"],
)
def test_failed_attempts_keep_cooldown_across_restart(client, error):
    opener, clock = client
    opener.open.side_effect = error
    assert text(module()) == "Tennis: unavailable"
    clock.return_value = 10899
    assert text(module()) == "Tennis: unavailable"
    assert opener.open.call_count == 1
    clock.return_value = 10900
    text(module())
    assert opener.open.call_count == 2


def test_failed_refresh_retains_and_marks_snapshot(client):
    opener, clock = client
    mod = module()
    original = text(mod)
    clock.return_value = 10900
    opener.open.side_effect = urllib.error.URLError("offline")
    assert text(mod) == original + " (stale)"
    assert mod.state(None) == ["warning"]
    clock.return_value = 11799
    assert text(module()) == original + " (stale)"
    assert opener.open.call_count == 2
    clock.return_value = 11800
    opener.open.side_effect = lambda *args, **kwargs: io.StringIO('{"data": []}')
    assert text(mod) == "Tennis: no live match"
    assert mod.state(None) == []


def test_independent_keys_do_not_share_scores(client, monkeypatch):
    text(module())
    monkeypatch.setenv("OTHER_TENNIS_KEY", "other-unit-key")
    text(module("livetennis.key_env=OTHER_TENNIS_KEY"))
    assert client[0].open.call_count == 2


def test_match_selection_uses_shared_listing(client):
    opener, clock = client
    data = [match(1), match(2)]
    data[1]["players"]["p1"]["name"] = "Third"
    opener.open.side_effect = lambda *args, **kwargs: io.StringIO(
        json.dumps({"data": data})
    )
    assert "First" in text(module())
    assert "Third" in text(module("livetennis.match=2"))
    assert text(module("livetennis.match=3")) == "Tennis: no live match"
    assert opener.open.call_count == 1


@pytest.mark.parametrize(
    "score,expected",
    [
        (None, "First v Second (score unavailable)"),
        ({"games": None, "points": ["0", "0"]}, "First v Second (score unavailable)"),
        ({"games": [], "points": [None, None], "server": None}, "First v Second"),
        (
            {"games": [[6, 3], [4, 4]], "points": ["15", "30"], "server": 1},
            "First* v Second 6-4 3-4 (15-30)",
        ),
        (
            {"games": [[6], [6]], "points": ["4", "2"], "is_tiebreak": True},
            "First v Second 6-6 (TB 4-2)",
        ),
        (
            {
                "games": [[6, 4, 10], [4, 6, 5]],
                "points": [None, None],
                "is_tiebreak": True,
            },
            "First v Second 6-4 4-6 [10-5]",
        ),
        (
            {"games": [[0], [0]], "points": ["0", None], "server": 2},
            "First v Second* 0-0",
        ),
    ],
)
def test_score_format_uses_player_major_games(client, score, expected):
    client[0].open.side_effect = lambda *args, **kwargs: io.StringIO(
        json.dumps({"data": [match(score=score)]})
    )
    assert text(module()) == "Tennis: " + expected


def test_unwritable_cache_does_not_call_api(client):
    with mock.patch.object(
        livetennis, "save_snapshot", side_effect=OSError("read only")
    ):
        assert text(module()) == "Tennis: cache unavailable"
    client[0].open.assert_not_called()


def test_corrupt_cache_does_not_reset_budget(client, tmp_path):
    text(module())
    path = next(tmp_path.rglob("*.json"))
    path.write_text("not JSON")
    assert text(module()) == "Tennis: cache unavailable"
    assert client[0].open.call_count == 1


def test_attempt_is_saved_before_request(client):
    opener, clock = client
    opener.open.side_effect = KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        text(module())
    clock.return_value = 10899
    assert text(module()) == "Tennis: unavailable"
    assert opener.open.call_count == 1


def test_daily_attempts_stay_within_free_allowance(client):
    opener, clock = client
    opener.open.side_effect = urllib.error.URLError("offline")
    mod = module("livetennis.interval=0.1")
    for seconds in range(0, 86400, 60):
        clock.return_value = 10000 + seconds
        text(mod)
    assert opener.open.call_count == 96


@pytest.mark.parametrize("timestamp", [-1, True, "yesterday", float("nan")])
def test_invalid_timestamp_does_not_reset_budget(client, tmp_path, timestamp):
    text(module())
    path = next(tmp_path.rglob("*.json"))
    saved = json.loads(path.read_text())
    saved["attempt"] = timestamp
    path.write_text(json.dumps(saved))
    assert text(module()) == "Tennis: cache unavailable"
    assert client[0].open.call_count == 1


def test_concurrent_widgets_share_one_request(client):
    opener, clock = client
    barrier = threading.Barrier(4)
    modules = [module() for _ in range(4)]

    def update(mod):
        barrier.wait(timeout=10)
        return text(mod)

    with ThreadPoolExecutor(max_workers=4) as pool:
        outputs = list(pool.map(update, modules))
    assert len(set(outputs)) == 1
    assert opener.open.call_count == 1


def test_redirects_cannot_forward_key_or_add_requests():
    request = livetennis.urllib.request.Request(
        livetennis.URL, headers={"X-API-Key": "unit-test-key"}
    )
    assert (
        livetennis.NoRedirect().redirect_request(
            request, None, 302, "moved", {}, "https://example.org/"
        )
        is None
    )
