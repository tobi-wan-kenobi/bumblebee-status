"""Displays tennis score snapshots from Live Tennis API using a free key.

Set the LIVETENNIS_API_KEY environment variable before starting the bar.
Only the free live match listing is requested. Snapshots refresh at most
once every 15 minutes, including failed requests. Aliases and restarts share
the request budget for the same key, user and state directory on this host.
Other clients consume the same daily allowance of 100 requests.

The cache is stored under XDG_STATE_HOME, or ~/.local/state. If it cannot
be read or written, the module stops making requests. Cached scores are
marked stale after a failed refresh. An asterisk identifies the server.

Parameters:
    * livetennis.key_env: Environment variable containing the API key.
      Defaults to LIVETENNIS_API_KEY.
    * livetennis.match: Match ID to display. Defaults to the first live match.
    * livetennis.interval: Display update interval. Defaults to 60 seconds.
      Shorter intervals cannot increase the request rate.
"""

import fcntl
import hashlib
import json
import math
import os
import tempfile
import time
import urllib.error
import urllib.request

import core.decorators
import core.module
import core.widget

URL = "https://api.livetennisapi.com/api/public/v1/matches?status=live"
# 86400 / 900 = 96 attempts per day, shared by every widget using this key.
MIN_INTERVAL = 900


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        # A redirect must not forward the API key or spend another request.
        return None


def save_snapshot(path, snapshot):
    fd, temporary = tempfile.mkstemp(dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(snapshot, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(os.path.dirname(path), os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_snapshot(key):
    root = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    directory = os.path.join(root, "bumblebee-status", "livetennis")
    os.makedirs(directory, mode=0o700, exist_ok=True)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    path = os.path.join(directory, digest + ".json")
    fd = os.open(path + ".lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            with open(path) as stream:
                snapshot = json.load(stream)
        except FileNotFoundError:
            snapshot = {"attempt": 0, "data": None, "error": True}

        attempt = snapshot["attempt"]
        if (
            isinstance(attempt, bool)
            or not isinstance(attempt, (int, float))
            or not math.isfinite(attempt)
            or attempt < 0
        ):
            raise ValueError("Invalid cache timestamp")
        now = time.time()
        if attempt and now - attempt < MIN_INTERVAL:
            return snapshot

        snapshot["attempt"] = now
        snapshot["error"] = True
        # Persist the attempt before networking, so a crash keeps the cooldown.
        save_snapshot(path, snapshot)
        try:
            request = urllib.request.Request(URL, headers={"X-API-Key": key})
            opener = urllib.request.build_opener(NoRedirect())
            with opener.open(request, timeout=10) as response:
                data = json.load(response)["data"]
            if not isinstance(data, list) or any(not isinstance(m, dict) for m in data):
                raise ValueError("Invalid match list")
            snapshot["data"] = data
            snapshot["error"] = False
        except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError):
            pass
        save_snapshot(path, snapshot)
        return snapshot


def match_text(match):
    players = match.get("players") or {}
    names = [
        " ".join((players.get(p) or {}).get("name", "?").split()) for p in ("p1", "p2")
    ]
    score = match.get("score") or {}
    server = score.get("server")
    if server in (1, 2):
        names[server - 1] += "*"
    result = "{} v {}".format(*names)
    games = score.get("games")
    if games is None:
        return result + " (score unavailable)"
    sets = []
    if len(games) == 2:
        for first, second in zip(games[0], games[1]):
            sets.append("{}-{}".format(first, second))
        if sets and score.get("is_tiebreak") and max(games[0][-1], games[1][-1]) > 7:
            sets[-1] = "[{}]".format(sets[-1])
    if sets:
        result += " " + " ".join(sets)
    points = score.get("points") or []
    if len(points) == 2 and all(point is not None for point in points):
        label = "TB " if score.get("is_tiebreak") else ""
        result += " ({}{}-{})".format(label, *points)
    return result


class Module(core.module.Module):
    @core.decorators.every(seconds=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.livetennis))
        self.background = True
        self.__label = "Tennis: loading"
        self.__state = []

    def livetennis(self, widget):
        return self.__label

    def update(self):
        key = os.environ.get(
            self.parameter("key_env", "LIVETENNIS_API_KEY"), ""
        ).strip()
        self.__state = []
        if not key:
            self.__label = "Tennis: missing API key"
            self.__state = ["warning"]
            return
        try:
            snapshot = read_snapshot(key)
            data = snapshot["data"]
            if data is None:
                self.__label = "Tennis: unavailable"
            else:
                matches = [m for m in data if m.get("status") == "live"]
                selected = self.parameter("match")
                if selected:
                    matches = [m for m in matches if str(m.get("id")) == str(selected)]
                self.__label = "Tennis: " + (
                    match_text(matches[0]) if matches else "no live match"
                )
                if snapshot["error"]:
                    self.__label += " (stale)"
            if snapshot["error"]:
                self.__state = ["warning" if data is not None else "critical"]
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            self.__label = "Tennis: cache unavailable"
            self.__state = ["critical"]

    def state(self, widget):
        return self.__state
