"""Displays info about zpools present on the system

Requires the following executable:
    * sudo (if `zpool.sudo` is explicitly set to `true`)

Parameters:
   * zpool.list: Comma-separated list of zpools to display info for. If empty, info for all zpools
     is displayed. (Default: '')
   * zpool.format: Format string, tags {name}, {used}, {left}, {size}, {percentfree}, {percentuse},
     {status}, {shortstatus}, {fragpercent}, {deduppercent} are supported.
     (Default: '{name} {used}/{size} ({percentfree}%)')
   * zpool.showio: Show also widgets detailing current read and write I/O (Default: true)
   * zpool.ioformat: Format string for I/O widget, tags {ops} (operations per seconds) and {band}
     (bandwidth) are supported. (Default: '{band}')
   * zpool.warnfree: Warn if free space is below this percentage (Default: 10)
   * zpool.sudo: Use sudo when calling the `zpool` binary. (Default: false)

Option `zpool.sudo` is intended for Linux users using zfsonlinux older than 0.7.0: In pre-0.7.0
releases of zfsonlinux regular users couldn't invoke even informative commands such as
`zpool list`. If this option is true, command `zpool list` is invoked with sudo. If this option
is used, the following (or ekvivalent) must be added to the `sudoers(5)`:

```
<username/ALL> ALL = (root) NOPASSWD: /usr/bin/zpool list
```

Be aware of security implications of doing this!

contributed by `adam-dej <https://github.com/adam-dej>`_ - many thanks!
"""

import time
import logging
from pkg_resources import parse_version

log = logging.getLogger(__name__)

import core.module

import util.cli
import util.format


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self._includelist = set(
            filter(
                lambda x: len(x) > 0,
                util.format.aslist(self.parameter("list", default="")),
            )
        )
        self._format = self.parameter(
            "format", default="{name} {shortstatus} {used}/{size} " + "({percentfree}%)"
        )
        self._usesudo = util.format.asbool(self.parameter("sudo", default=False))
        self._showio = util.format.asbool(self.parameter("showio", default=True))
        self._ioformat = self.parameter("ioformat", default="{band}")
        self._warnfree = int(self.parameter("warnfree", default=10))

    def update(self):
        self.clear_widgets()
        zfs_version_path = "/sys/module/zfs/version"
        # zpool list -H: List all zpools, use script mode (no headers and tabs as separators).
        try:
            with open(zfs_version_path, "r") as zfs_mod_version:
                zfs_version = zfs_mod_version.readline().rstrip().split("-")[0]
        except IOError:
            # ZFS isn't installed or the module isn't loaded, stub the version
            zfs_version = "0.0.0"
            logging.error(
                "ZFS version information not found at {}, check the module is loaded.".format(
                    zfs_version_path
                )
            )

        raw_zpools = util.cli.execute(
            ("sudo " if self._usesudo else "") + "zpool list -H"
        ).split("\n")

        for raw_zpool in raw_zpools:
            try:
                # Ignored fields (assigned to _) are 'expandsz' and 'altroot', also 'ckpoint' in ZFS 0.8.0+
                if parse_version(zfs_version) < parse_version("0.8.0"):
                    (
                        name,
                        size,
                        alloc,
                        free,
                        _,
                        frag,
                        cap,
                        dedup,
                        health,
                        _,
                    ) = raw_zpool.split("\t")
                else:
                    (
                        name,
                        size,
                        alloc,
                        free,
                        _,
                        _,
                        frag,
                        cap,
                        dedup,
                        health,
                        _,
                    ) = raw_zpool.split("\t")
                cap = cap.rstrip("%")
                percentuse = int(cap)
                percentfree = 100 - percentuse
                # There is a command, zpool iostat, which is however blocking and was therefore
                # causing issues.
                # Instead, we read file `/proc/spl/kstat/zfs/<poolname>/io` which contains
                # cumulative I/O statistics since boot (or pool creation). We store these values
                # (and timestamp) during each widget update, and during the next widget update we
                # use them to compute delta of transferred bytes, and using the last and current
                # timestamp the rate at which they have been transferred.
                with open("/proc/spl/kstat/zfs/{}/io".format(name), "r") as f:
                    # Third row provides data we need, we are interested in the first 4 values.
                    # More info about this file can be found here:
                    # https://github.com/zfsonlinux/zfs/blob/master/lib/libspl/include/sys/kstat.h#L580
                    # The 4 values are:
                    # nread, nwritten, reads, writes
                    iostat = list(map(int, f.readlines()[2].split()[:4]))
            except (ValueError, IOError):
                # Unable to parse info about this pool, skip it
                continue

            if self._includelist and name not in self._includelist:
                continue

            widget = self.widget(name)
            if not widget:
                widget = self.add_widget(name=name)
                widget.set("last_iostat", [0, 0, 0, 0])
                widget.set("last_timestamp", 0)

            delta_iostat = [b - a for a, b in zip(iostat, widget.get("last_iostat"))]
            widget.set("last_iostat", iostat)

            # From docs:
            #   > Note that even though the time is always returned as a floating point number, not
            #   > all systems provide time with a better precision than 1 second.
            # Be aware that that may affect the precision of reported I/O
            # Also, during one update cycle the reported I/O may be garbage if the system time
            # was changed.
            timestamp = time.time()
            delta_timestamp = widget.get("last_timestamp") - timestamp
            widget.set("last_timestamp", time.time())

            # abs is there because sometimes the result is -0
            rate_iostat = [abs(x / delta_timestamp) for x in delta_iostat]
            nread, nwritten, reads, writes = rate_iostat

            # theme.minwidth is not set since these values are not expected to change
            # rapidly
            widget.full_text(
                self._format.format(
                    name=name,
                    used=alloc,
                    left=free,
                    size=size,
                    percentfree=percentfree,
                    percentuse=percentuse,
                    status=health,
                    shortstatus=self._shortstatus(health),
                    fragpercent=frag,
                    deduppercent=dedup,
                )
            )
            widget.set("state", health)
            widget.set("percentfree", percentfree)
            widget.set("visited", True)

            if self._showio:
                wname, rname = [name + x for x in ["__write", "__read"]]
                widget_w = self.widget(wname)
                widget_r = self.widget(rname)
                if not widget_w or not widget_r:
                    widget_r = self.add_widget(name=rname)
                    widget_w = self.add_widget(name=wname)
                for w in [widget_r, widget_w]:
                    w.set(
                        "theme.minwidth",
                        self._ioformat.format(
                            ops=9999, band=util.format.bytefmt(999.99 * (1024 ** 2))
                        ),
                    )
                widget_w.full_text(
                    self._ioformat.format(
                        ops=round(writes), band=util.format.bytefmt(nwritten)
                    )
                )
                widget_r.full_text(
                    self._ioformat.format(
                        ops=round(reads), band=util.format.bytefmt(nread)
                    )
                )

    def state(self, widget):
        if widget.name.endswith("__read"):
            return "poolread"
        elif widget.name.endswith("__write"):
            return "poolwrite"

        state = widget.get("state")
        if state == "FAULTED":
            return [state, "critical"]
        elif state == "DEGRADED" or widget.get("percentfree") < self._warnfree:
            return [state, "warning"]

        return state

    @staticmethod
    def _shortstatus(status):
        # From `zpool(8)`, section Device Failure and Recovery:
        # A pool's health status is described by one of three states: online, degraded, or faulted.
        # An online pool has all devices operating normally.  A degraded pool is one in which one
        # or more devices have failed, but the data is still available due to a redundant
        # configuration.  A faulted pool has corrupted metadata, or one or more faulted devices, and
        # insufficient replicas to continue functioning.
        shortstate = {
            "DEGRADED": "DEG",
            "FAULTED": "FLT",
            "ONLINE": "ONL",
        }
        try:
            return shortstate[status]
        except KeyError:
            return ""


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
