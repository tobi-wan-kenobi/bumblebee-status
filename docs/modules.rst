List of available modules
=========================

+--------------------+-------------------------------------------------+
| Name               | Description                                     |
+====================+=================================================+
| \__pulseaudio      | Displays volume and mute status and controls    |
|                    | for PulseAudio devices. Use wheel up and down   |
|                    | to change volume, left click mutes, right click |
|                    | opens pavucontrol.Aliases: pasink (use this to  |
|                    | control output instead of input),               |
|                    | pasourceParameters: \* pulseaudio.autostart: If |
|                    | set to ‘true’ (default is ‘false’),             |
|                    | automatically starts the pulseaudio daemon if   |
|                    | it is not running \* pulseaudio.percent_change: |
|                    | How much to change volume by when scrolling on  |
|                    | the module (default is 2%) \* pulseaudio.limit: |
|                    | Upper limit for setting the volume (default is  |
|                    | 0%, which means ‘no limit’) Note: If the left   |
|                    | and right channels have different volumes, the  |
|                    | limit might not be reached exactly. \*          |
|                    | pulseaudio.showbars: 1 for showing volume bars, |
|                    | requires –markup=pango; 0 for not showing       |
|                    | volume bars (default)Requires the following     |
|                    | executable: \* pulseaudio \* pactl \*           |
|                    | pavucontrol                                     |
+--------------------+-------------------------------------------------+

\|amixer \|get volume levelParameters: \* amixer.device: Device to use,
defaults to “Master,0”

.. raw:: html

   <p />

.. raw:: html

   <p />

|amixer| \| \|apt \|Displays APT package update information (<to
upgrade>/<to remove >)Requires the following packages: \* aptitude \|
\|arch-update \|Check updates to Arch Linux.Requires the following
executable: \* checkupdates (from pacman-contrib) \| \|battery
\|Displays battery status, remaining percentage and charging
information.Parameters: \* battery.device : Comma-separated list of
battery devices to read information from (defaults to auto for
auto-detection) \* battery.warning : Warning threshold in % of remaining
charge (defaults to 20) \* battery.critical : Critical threshold in % of
remaining charge (defaults to 10) \* battery.showdevice : If set to
‘true’, add the device name to the widget (defaults to False) \*
battery.decorate : If set to ‘false’, hides additional icons (charging,
etc.) (defaults to True) \* battery.showpowerconsumption: If set to
‘true’, show current power consumption (defaults to False) \*
battery.compact-devices : If set to ‘true’, compacts multiple batteries
into a single entry (default to False)

.. raw:: html

   <p />

.. raw:: html

   <p />

|battery| \| \|battery-upower \|Displays battery status, remaining
percentage and charging information.Parameters: \*
battery-upower.warning : Warning threshold in % of remaining charge
(defaults to 20) \* battery-upower.critical : Critical threshold in % of
remaining charge (defaults to 10) \* battery-upower.showremaining : If
set to true (default) shows the remaining time until the batteries are
completely discharged \| \|bluetooth \|Displays bluetooth status
(Bluez). Left mouse click launches manager app,right click toggles
bluetooth. Needs dbus-send to toggle bluetooth state.Parameters: \*
bluetooth.device : the device to read state from (default is hci0) \*
bluetooth.manager : application to launch on click (blueman-manager) \*
bluetooth.dbus_destination : dbus destination (defaults to
org.blueman.Mechanism) \* bluetooth.dbus_destination_path : dbus
destination path (defaults to /) \* bluetooth.right_click_popup : use
popup menu when right-clicked (defaults to True)

.. raw:: html

   <p />

.. raw:: html

   <p />

|bluetooth| \| \|bluetooth2 \|Displays bluetooth status. Left mouse
click launches manager app,right click toggles bluetooth. Needs
dbus-send to toggle bluetooth state andpython-dbus to count the number
of connectionsParameters: \* bluetooth.manager : application to launch
on click (blueman-manager) \| \|brightness \|Displays the brightness of
a displayParameters: \* brightness.step: The amount of increase/decrease
on scroll in % (defaults to 2)

.. raw:: html

   <p />

.. raw:: html

   <p />

|brightness| \| \|caffeine \|Enable/disable automatic screen
locking.Requires the following executables: \* xdg-screensaver \*
xdotool \* xprop (as dependency for xdotool) \* notify-send

.. raw:: html

   <p />

.. raw:: html

   <p />

|caffeine| \| \|cmus \|Displays information about the current song in
cmus.Requires the following executable: \* cmus-remoteParameters: \*
cmus.format: Format string for the song information. Tag values can be
put in curly brackets (i.e. {artist}) Additional tags: \* {file} - full
song file name \* {file1} - song file name without path prefix if {file}
= ‘/foo/bar.baz’, then {file1} = ‘bar.baz’ \* {file2} - song file name
without path prefix and extension suffix if {file} = ‘/foo/bar.baz’,
then {file2} = ‘bar’ \* cmus.layout: Space-separated list of widgets to
add. Possible widgets are the buttons/toggles cmus.prev, cmus.next,
cmus.shuffle and cmus.repeat, and the main display with play/pause
function cmus.main. \* cmus.server: The address of the cmus server,
either a UNIX socket or host[:port]. Connects to the local instance by
default. \* cmus.passwd: The password to use for the TCP/IP connection.

.. raw:: html

   <p />

.. raw:: html

   <p />

|cmus| \| \|cpu \|Displays CPU utilization across all CPUs.Parameters:
\* cpu.warning : Warning threshold in % of CPU usage (defaults to 70%)
\* cpu.critical: Critical threshold in % of CPU usage (defaults to 80%)
\* cpu.format : Format string (defaults to ‘{:.01f}%’)

.. raw:: html

   <p />

.. raw:: html

   <p />

|cpu| \| \|cpu2 \|Multiwidget CPU moduleCan display any combination of:
\* max CPU frequency \* total CPU load in percents (integer value) \*
per-core CPU load as graph - either mono or colored \* CPU temperature
(in Celsius degrees) \* CPU fan speedRequirements: \* the psutil Python
module for the first three items from the list above \* sensors
executable for the restParameters: \* cpu2.layout: Space-separated list
of widgets to add. Possible widgets are: \* cpu2.maxfreq \* cpu2.cpuload
\* cpu2.coresload \* cpu2.temp \* cpu2.fanspeed \* cpu2.colored: 1 for
colored per core load graph, 0 for mono (default) if this is set to 1,
use –markup=pango \* cpu2.temp_pattern: pattern to look for in the
output of ‘sensors -u’; required if cpu2.temp widged is used \*
cpu2.fan_pattern: pattern to look for in the output of ‘sensors -u’;
required if cpu2.fanspeed widged is usedNote: if you are getting ‘n/a’
for CPU temperature / fan speed, then you’relacking the aforementioned
pattern settings or they have wrong values. \| \|currency \|Displays
currency exchange rates. Currently, displays currency between GBP and
USD/EUR only.Requires the following python packages: \*
requestsParameters: \* currency.interval: Interval in minutes between
updates, default is 1. \* currency.source: Source currency (ex. ‘GBP’,
‘EUR’). Defaults to ‘auto’, which infers the local one from IP address.
\* currency.destination: Comma-separated list of destination currencies
(defaults to ‘USD,EUR’) \* currency.sourceformat: String format for
source formatting; Defaults to ‘{}: {}’ and has two variables, the base
symbol and the rate list \* currency.destinationdelimiter: Delimiter
used for separating individual rates (defaults to ‘\|’)Note: source and
destination names right now must correspond to the names used by the API
of https://markets.ft.com

.. raw:: html

   <p />

.. raw:: html

   <p />

|currency| \| \|date \|Displays the current date and time.Parameters: \*
date.format: strftime()-compatible formatting string \* date.locale:
locale to use rather than the system default

.. raw:: html

   <p />

.. raw:: html

   <p />

|date| \| \|datetime \|Displays the current date and time.Parameters: \*
datetime.format: strftime()-compatible formatting string \*
datetime.locale: locale to use rather than the system default

.. raw:: html

   <p />

.. raw:: html

   <p />

|datetime| \| \|datetimetz \|Displays the current date and time with
timezone options.Parameters: \* datetimetz.format :
strftime()-compatible formatting string \* datetimetz.timezone : IANA
timezone name \* datetz.format : alias for datetimetz.format \*
timetz.format : alias for datetimetz.format \* timetz.timezone : alias
for datetimetz.timezone \* datetimetz.locale : locale to use rather than
the system default \* datetz.locale : alias for datetimetz.locale \*
timetz.locale : alias for datetimetz.locale \* timetz.timezone : alias
for datetimetz.timezone \| \|datetz \|Displays the current date and
time.Parameters: \* date.format: strftime()-compatible formatting string
\* date.locale: locale to use rather than the system default \|
\|deadbeef \|Displays the current song being played in DeaDBeeF and
providessome media control bindings.Left click toggles pause, scroll up
skips the current song, scrolldown returns to the previous song.Requires
the following library: \* subprocessParameters: \* deadbeef.format:
Format string (defaults to ‘{artist} - {title}’) Available values are:
{artist}, {title}, {album}, {length}, {trackno}, {year}, {comment},
{copyright}, {time} This is deprecated, but much simpler. \*
deadbeef.tf_format: A foobar2000 title formatting-style format string.
These can be much more sophisticated than the standard format strings.
This is off by default, but specifying any tf_format will enable it. If
both deadbeef.format and deadbeef.tf_format are specified,
deadbeef.tf_format takes priority. \* deadbeef.tf_format_if_stopped:
Controls whether or not the tf_format format string should be displayed
even if no song is paused or playing. This could be useful if you want
to implement your own stop strings with the built in logic. Any non-
null value will enable this (by default the module will hide itself when
the player is stopped). \* deadbeef.previous: Change binding for
previous song (default is left click) \* deadbeef.next: Change binding
for next song (default is right click) \* deadbeef.pause: Change binding
for toggling pause (default is middle click) Available options for
deadbeef.previous, deadbeef.next and deadbeef.pause are: LEFT_CLICK,
RIGHT_CLICK, MIDDLE_CLICK, SCROLL_UP, SCROLL_DOWN \| \|debug \|Shows
that debug is enabled \| \|deezer \|Displays the current song being
playedRequires the following library: \* python-dbusParameters: \*
deezer.format: Format string (defaults to ‘{artist} - {title}’)
Available values are: {album}, {title}, {artist}, {trackNumber},
{playbackStatus} \* deezer.previous: Change binding for previous song
(default is left click) \* deezer.next: Change binding for next song
(default is right click) \* deezer.pause: Change binding for toggling
pause (default is middle click) Available options for deezer.previous,
deezer.next and deezer.pause are: LEFT_CLICK, RIGHT_CLICK, MIDDLE_CLICK,
SCROLL_UP, SCROLL_DOWN \| \|disk \|Shows free diskspace, total diskspace
and the percentage of free disk space.Parameters: \* disk.warning:
Warning threshold in % of disk space (defaults to 80%) \* disk.critical:
Critical threshold in % of disk space (defaults ot 90%) \* disk.path:
Path to calculate disk usage from (defaults to /) \* disk.open: Which
application / file manager to launch (default xdg-open) \* disk.format:
Format string, tags {path}, {used}, {left}, {size} and {percent}
(defaults to ‘{path} {used}/{size} ({percent:05.02f}%)’)

.. raw:: html

   <p />

.. raw:: html

   <p />

|disk| \| \|dnf \|Displays DNF package update information
(<security>/<bugfixes>/<enhancements>/<other>)Requires the following
executable: \* dnfParameters: \* dnf.interval: Time in minutes between
two consecutive update checks (defaults to 30 minutes)

.. raw:: html

   <p />

.. raw:: html

   <p />

|dnf| \| \|docker_ps \|Displays the number of docker containers
runningRequires the following python packages: \* docker \| \|dunst
\|Toggle dunst notifications.

.. raw:: html

   <p />

.. raw:: html

   <p />

|dunst| \| \|error \|Shows bumblebee-status errors \| \|getcrypto
\|Displays the price of a cryptocurrency.Requires the following python
packages: \* requestsParameters: \* getcrypto.interval: Interval in
seconds for updating the price, default is 120, less than that will
probably get your IP banned. \* getcrypto.getbtc: 0 for not getting
price of BTC, 1 for getting it (default). \* getcrypto.geteth: 0 for not
getting price of ETH, 1 for getting it (default). \* getcrypto.getltc: 0
for not getting price of LTC, 1 for getting it (default). \*
getcrypto.getcur: Set the currency to display the price in, usd is the
default.

.. raw:: html

   <p />

.. raw:: html

   <p />

|getcrypto| \| \|git \|Print the branch and git status for thecurrently
focused window.Requires: \* xcwd \* Python module ‘pygit2’

.. raw:: html

   <p />

.. raw:: html

   <p />

|git| \| \|github \|Displays the unread GitHub notifications for a
GitHub userRequires the following library: \* requestsParameters: \*
github.token: GitHub user access token, the token needs to have the
‘notifications’ scope. \* github.interval: Interval in minutes between
updates, default is 5.

.. raw:: html

   <p />

.. raw:: html

   <p />

|github| \| \|gpmdp \|Displays information about the current song in
Google Play music player.Requires the following executable: \*
gpmdp-remote \| \|hddtemp \|Fetch hard drive temeperature data from a
hddtemp daemonthat runs on localhost and default port (7634) \|
\|hostname \|Displays the system hostname. \| \|http_status \|Display
HTTP status codeParameters: \* http__status.label: Prefix label
(optional) \* http__status.target: Target to retrieve the HTTP status
from \* http__status.expect: Expected HTTP status

.. raw:: html

   <p />

.. raw:: html

   <p />

|http_status| \| \|indicator \|Displays the indicator status, for
numlock, scrolllock and capslock Parameters: \* indicator.include:
Comma-separated list of interface prefixes to include (defaults to
‘numlock,capslock’) \* indicator.signalstype: If you want the signali
type color to be ‘critical’ or ‘warning’ (defaults to ‘warning’)

.. raw:: html

   <p />

.. raw:: html

   <p />

|indicator| \| \|kernel \|Shows Linux kernel version information

.. raw:: html

   <p />

.. raw:: html

   <p />

|kernel| \| \|layout \|Displays and changes the current keyboard
layoutRequires the following executable: \* setxkbmap

.. raw:: html

   <p />

.. raw:: html

   <p />

|layout| \| \|layout-xkb \|Displays the current keyboard layout using
libX11Requires the following library: \* libX11.so.6and python module:
\* xkbgroupParameters: \* layout-xkb.showname: Boolean that indicate
whether the full name should be displayed. Defaults to false (only the
symbol will be displayed) \* layout-xkb.show_variant: Boolean that
indecates whether the variant name should be displayed. Defaults to
true. \| \|layout-xkbswitch \|Displays and changes the current keyboard
layoutRequires the following executable: \* xkb-switch \| \|libvirtvms
\|Displays count of running libvirt VMs.Required the following python
packages: \* libvirt \| \|load \|Displays system load.Parameters: \*
load.warning : Warning threshold for the one-minute load average
(defaults to 70% of the number of CPUs) \* load.critical: Critical
threshold for the one-minute load average (defaults to 80% of the number
of CPUs)

.. raw:: html

   <p />

.. raw:: html

   <p />

|load| \| \|memory \|Displays available RAM, total amount of RAM and
percentage available.Parameters: \* memory.warning : Warning threshold
in % of memory used (defaults to 80%) \* memory.critical: Critical
threshold in % of memory used (defaults to 90%) \* memory.format: Format
string (defaults to ‘{used}/{total} ({percent:05.02f}%)’) \*
memory.usedonly: Only show the amount of RAM in use (defaults to False).
Same as memory.format=‘{used}’

.. raw:: html

   <p />

.. raw:: html

   <p />

|memory| \| \|mocp \|Displays information about the current song in
mocp. Left click toggles play/pause. Right click toggles
shuffle.Requires the following executable: \* mocpParameters: \*
mocp.format: Format string for the song information. Replace string
sequences with the actual information: %state State %file File %title
Title, includes track, artist, song title and album %artist Artist %song
SongTitle %album Album %tt TotalTime %tl TimeLeft %ts TotalSec %ct
CurrentTime %cs CurrentSec %b Bitrate %r Sample rate \| \|mpd \|Displays
information about the current song in mpd.Requires the following
executable: \* mpcParameters: \* mpd.format: Format string for the song
information. Supported tags (see ``man mpc`` for additional information)
\* {name} \* {artist} \* {album} \* {albumartist} \* {comment} \*
{composer} \* {date} \* {originaldate} \* {disc} \* {genre} \*
{performer} \* {title} \* {track} \* {time} \* {file} \* {id} \* {prio}
\* {mtime} \* {mdate} Additional tags: \* {position} - position of
currently playing song not to be confused with %position% mpc tag \*
{duration} - duration of currently playing song \* {file1} - song file
name without path prefix if {file} = ‘/foo/bar.baz’, then {file1} =
‘bar.baz’ \* {file2} - song file name without path prefix and extension
suffix if {file} = ‘/foo/bar.baz’, then {file2} = ‘bar’ \* mpd.host: MPD
host to connect to. (mpc behaviour by default) \* mpd.layout:
Space-separated list of widgets to add. Possible widgets are the
buttons/toggles mpd.prev, mpd.next, mpd.shuffle and mpd.repeat, and the
main display with play/pause function mpd.main.

.. raw:: html

   <p />

.. raw:: html

   <p />

|mpd| \| \|network_traffic \|Displays network traffic\* No extra
configuration needed \| \|nic \|Displays the name, IP address(es) and
status of each available network interface.Requires the following python
module: \* netifacesParameters: \* nic.exclude: Comma-separated list of
interface prefixes to exclude (defaults to
‘lo,virbr,docker,vboxnet,veth,br’) \* nic.include: Comma-separated list
of interfaces to include \* nic.states: Comma-separated list of states
to show (prefix with ‘^’ to invert - i.e. ^down -> show all devices that
are not in state down) \* nic.format: Format string (defaults to ‘{intf}
{state} {ip} {ssid}’)

.. raw:: html

   <p />

.. raw:: html

   <p />

|nic| \| \|notmuch_count \|Displays the result of a notmuch count query
default : unread emails which path do not contained ‘Trash’ (notmuch
count ‘tag:unread AND NOT path:/.\ *Trash.*/’)Parameters: \*
notmuch_count.query: notmuch count query to show result Errors: if the
notmuch query failed, the shown value is -1Dependencies: notmuch
(https://notmuchmail.org/) \| \|nvidiagpu \|Displays GPU name,
temperature and memory usage.Parameters: \* nvidiagpu.format: Format
string (defaults to ‘{name}: {temp}°C %{usedmem}/{totalmem} MiB’)
Available values are: {name} {temp} {mem_used} {mem_total} {fanspeed}
{clock_gpu} {clock_mem}Requires nvidia-smi \| \|octoprint \|Displays the
Octorpint status and the printer’s bed/tools temperature in the status
bar. Left click opens a popup which shows the bed & tools temperatures
and additionally a livestream of the webcam (if enabled).Parameters: \*
octoprint.address : Octoprint address (e.q: http://192.168.1.3) \*
octoprint.apitoken : Octorpint API Token (can be obtained from the
Octoprint Webinterface) \* octoprint.webcam : Set to True if a webcam is
connected (default: False) \| \|pacman \|Displays update information per
repository for pacman.Parameters: \* pacman.sum: If you prefere
displaying updates with a single digit (defaults to ‘False’)Requires the
following executables: \* fakeroot \* pacman

.. raw:: html

   <p />

.. raw:: html

   <p />

|pacman| \| \|pihole \|Displays the pi-hole status (up/down) together
with the number of ads that were blocked todayParameters: \*
pihole.address : pi-hole address (e.q: http://192.168.1.3) \*
pihole.pwhash : pi-hole webinterface password hash (can be obtained from
the /etc/pihole/SetupVars.conf file) \| \|ping \|Periodically checks the
RTT of a configurable host using ICMP echosRequires the following
executable: \* pingParameters: \* ping.address : IP address to check \*
ping.timeout : Timeout for waiting for a reply (defaults to 5.0) \*
ping.probes : Number of probes to send (defaults to 5) \* ping.warning :
Threshold for warning state, in seconds (defaults to 1.0) \*
ping.critical: Threshold for critical state, in seconds (defaults to
2.0)

.. raw:: html

   <p />

.. raw:: html

   <p />

|ping| \| \|pomodoro \|Display and run a Pomodoro timer.Left click to
start timer, left click again to pause.Right click will cancel the
timer.Parameters: \* pomodoro.work: The work duration of timer in
minutes (defaults to 25) \* pomodoro.break: The break duration of timer
in minutes (defaults to 5) \* pomodoro.format: Timer display format with
‘%m’ and ‘%s’ for minutes and seconds (defaults to ‘%m:%s’) Examples:
‘%m min %s sec’, ‘%mm’, ’‘, ’timer’ \* pomodoro.notify: Notification
command to run when timer ends/starts (defaults to nothing) Example:
‘notify-send ’Time up!’‘. If you want to chain multiple commands, please
use an external wrapper script and invoke that. The module itself does
not support command chaining (see
https://github.com/tobi-wan-kenobi/bumblebee-status/issues/532 for a
detailled explanation) \| \|prime \|Displays and changes the current
selected prime video cardLeft click will call ’sudo prime-select
nvidia’Right click will call ‘sudo prime-select nvidia’Running these
commands without a password requires editing your sudoers file(always
use visudo, it’s very easy to make a mistake and get locked out of your
computer!)sudo visudo -f /etc/sudoers.d/primeThen put a line like this
in there: user ALL=(ALL) NOPASSWD: /usr/bin/prime-selectIf you can’t
figure out the sudoers thing, then don’t worry, it’s still really
useful.Parameters: \* prime.nvidiastring: String to use when nvidia is
selected (defaults to ‘intel’) \* prime.intelstring: String to use when
intel is selected (defaults to ‘intel’)Requires the following
executable: \* prime-select \| \|progress \|Show progress for cp, mv,
dd, …Parameters: \* progress.placeholder: Text to display while no
process is running (defaults to ‘n/a’) \* progress.barwidth: Width of
the progressbar if it is used (defaults to 8) \* progress.format: Format
string (defaults to ‘{bar} {cmd} {arg}’) Available values are: {bar}
{pid} {cmd} {arg} {percentage} {quantity} {speed} {time} \*
progress.barfilledchar: Character used to draw the filled part of the
bar (defaults to ‘#’), notice that it can be a string \*
progress.baremptychar: Character used to draw the empty part of the bar
(defaults to ‘-’), notice that it can be a stringRequires the following
executable: \* progress \| \|publicip \|Displays public IP address \|
\|redshift \|Displays the current color temperature of redshiftRequires
the following executable: \* redshiftParameters: \* redshift.location :
location provider, either of ‘auto’ (default), ‘geoclue2’, ‘ipinfo’ or
‘manual’ ‘auto’ uses whatever redshift is configured to do \*
redshift.lat : latitude if location is set to ‘manual’ \* redshift.lon :
longitude if location is set to ‘manual’

.. raw:: html

   <p />

.. raw:: html

   <p />

|redshift| \| \|rotation \|Shows a widget for each connected screen and
allows the user to loop through different orientations.Requires the
following executable: \* xrandr \| \|rss \|RSS news tickerFetches rss
news items and shows these as a news ticker.Left-clicking will open the
full story in a browser.New stories are highlighted.Parameters: \*
rss.feeds : Space-separated list of RSS URLs \* rss.length : Maximum
length of the module, default is 60 \| \|sensors \|Displays sensor
temperatureParameters: \* sensors.path: path to temperature file
(default /sys/class/thermal/thermal_zone0/temp). \* sensors.json: if set
to ‘true’, interpret sensors.path as JSON ‘path’ in the output of
‘sensors -j’ (i.e. <key1>/<key2>/…/<value>), for example, path could be:
‘coretemp-isa-00000/Core 0/temp1_input’ (defaults to ‘false’) \*
sensors.match: (fallback) Line to match against output of ‘sensors -u’
(default: temp1_input) \* sensors.match_pattern: (fallback) Line to
match against before temperature is read (no default) \*
sensors.match_number: (fallback) which of the matches you want (default
-1: last match). \* sensors.show_freq: whether to show CPU frequency.
(default: true)

.. raw:: html

   <p />

.. raw:: html

   <p />

|sensors| \| \|sensors2 \|Displays sensor temperature and CPU
frequencyParameters: \* sensors2.chip: ‘sensors -u’ compatible filter
for chip to display (default to empty - show all chips) \*
sensors2.showcpu: Enable or disable CPU frequency display (default:
true) \* sensors2.showtemp: Enable or disable temperature display
(default: true) \* sensors2.showfan: Enable or disable fan display
(default: true) \* sensors2.showother: Enable or display ‘other’ sensor
readings (default: false) \* sensors2.showname: Enable or disable show
of sensor name (default: false) \* sensors2.chip_include:
Comma-separated list of chip to include (defaults to ’’ will include all
by default, example: ‘coretemp,bat’) \* sensors2.chip_exclude:Comma
separated list of chip to exclude (defaults to ’’ will exlude none by
default) \* sensors2.field_include: Comma separated list of chip to
include (defaults to ’’ will include all by default, example:
‘temp,fan’) \* sensors2.field_exclude: Comma separated list of chip to
exclude (defaults to ’’ will exclude none by default) \*
sensors2.chip_field_exclude: Comma separated list of chip field to
exclude (defaults to ’’ will exclude none by default, example:
‘coretemp-isa-0000.temp1,coretemp-isa-0000.fan1’) \*
sensors2.chip_field_include: Comma-separated list of adaper field to
include (defaults to ’’ will include all by default)

.. raw:: html

   <p />

.. raw:: html

   <p />

|sensors2| \| \|shell \|Execute command in shell and print resultFew
command examples: ‘ping -c 1 1.1.1.1 \| grep
-Po’(?<=time=):raw-latex:`\d+`(.:raw-latex:`\d+`)? ms’‘ ’echo
’BTC=$(curl -s rate.sx/1BTC \| grep -Po’^:raw-latex:`\d+`‘)USD’‘ ’curl
-s https://wttr.in/London?format=%l+%t+%h+%w’ ‘pip3 freeze \| wc -l’
‘any_custom_script.sh \| grep arguments’Parameters: \* shell.command:
Command to execute Use single parentheses if evaluating anything inside
(sh-style) For example shell.command=‘echo $(date +’%H:%M:%S’)‘ But NOT
shell.command=’echo $(date +’%H:%M:%S’)‘ Second one will be evaluated
only once at startup \* shell.interval: Update interval in seconds
(defaults to 1s == every bumblebee-status update) \* shell.async: Run
update in async mode. Won’t run next thread if previous one didn’t
finished yet. Useful for long running scripts to avoid bumblebee-status
freezes (defaults to False) \| \|shortcut \|Shows a widget per
user-defined shortcut and allows to define the behaviourwhen clicking on
it.For more than one shortcut, the commands and labels are strings
separated bya demiliter (; semicolon by default).For example in order to
create two shortcuts labeled A and B with commandscmdA and cmdB you
could do: ./bumblebee-status -m shortcut -p shortcut.cmd=’ls;ps’
shortcut.label=‘A;B’Parameters: \* shortcut.cmds : List of commands to
execute \* shortcut.labels: List of widgets’ labels (text) \*
shortcut.delim : Commands and labels delimiter (; semicolon by default)

.. raw:: html

   <p />

.. raw:: html

   <p />

|shortcut| \| \|smartstatus \|Displays HDD smart status of different
drives or all drivesParameters: \* smartstatus.display: how to display
(defaults to ‘combined’, other choices: ‘seperate’ or ‘singles’) \*
smartstauts.drives: in the case of singles which drives to display,
separated comma list value, multiple accepted (defaults to ‘sda’,
example:‘sda,sdc’) \| \|spaceapi \|Displays the state of a Space API
endpointSpace API is an API for hackspaces based on JSON. See
spaceapi.io foran example.Requires the following libraries: \* requests
\* regexParameters: \* spaceapi.url: String representation of the api
endpoint \* spaceapi.format: Format string for the outputFormat Strings:
\* Format strings are indicated by double %% \* They represent a leaf in
the JSON tree, layers seperated by ‘.’ \* Boolean values can be
overwritten by appending ‘%true%false’ in the format string \* Example:
to reference ‘open’ in ‘{’state’:{‘open’: true}}‘ you would
write’%%state.open%%‘, if you also want to say ’Open/Closed’ depending
on the boolean you would write ‘%%state.open%Open%Closed%%’ \| \|spacer
\|Draws a widget with configurable text content.Parameters: \*
spacer.text: Widget contents (defaults to empty string)

.. raw:: html

   <p />

.. raw:: html

   <p />

|spacer| \| \|spotify \|Displays the current song being playedRequires
the following library: \* python-dbusParameters: \* spotify.format:
Format string (defaults to ‘{artist} - {title}’) Available values are:
{album}, {title}, {artist}, {trackNumber}, {playbackStatus} \*
spotify.previous: Change binding for previous song (default is left
click) \* spotify.next: Change binding for next song (default is right
click) \* spotify.pause: Change binding for toggling pause (default is
middle click) Available options for spotify.previous, spotify.next and
spotify.pause are: LEFT_CLICK, RIGHT_CLICK, MIDDLE_CLICK, SCROLL_UP,
SCROLL_DOWN

.. raw:: html

   <p />

.. raw:: html

   <p />

|spotify| \| \|stock \|Display a stock quote from
worldtradingdata.comRequires the following python packages: \*
requestsParameters: \* stock.symbols : Comma-separated list of symbols
to fetch \* stock.change : Should we fetch change in stock value
(defaults to True)

.. raw:: html

   <p />

.. raw:: html

   <p />

|stock| \| \|sun \|Displays sunrise and sunset timesRequires the
following python packages: \* requests \* suntimeParameters: \* cpu.lat
: Latitude of your location \* cpu.lon : Longitude of your location \|
\|system \|system moduleadds the possibility to \* shutdown \* rebootthe
system. Per default a confirmation dialog is shown before the actual
action is performed. Parameters: \* system.confirm: show confirmation
dialog before performing any action (default: true) \* system.reboot:
specify a reboot command (defaults to ‘reboot’) \* system.shutdown:
specify a shutdown command (defaults to ‘shutdown -h now’) \*
system.logout: specify a logout command (defaults to ‘i3exit logout’) \*
system.switch_user: specify a command for switching the user (defaults
to ‘i3exit switch_user’) \* system.lock: specify a command for locking
the screen (defaults to ‘i3exit lock’) \* system.suspend: specify a
command for suspending (defaults to ‘i3exit suspend’) \*
system.hibernate: specify a command for hibernating (defaults to ‘i3exit
hibernate’) \| \|taskwarrior \|Displays the number of pending tasks in
TaskWarrior.Requires the following library: \* taskwParameters: \*
taskwarrior.taskrc : path to the taskrc file (defaults to ~/.taskrc)

.. raw:: html

   <p />

.. raw:: html

   <p />

|taskwarrior| \| \|test \|Test module \| \|time \|Displays the current
date and time.Parameters: \* time.format: strftime()-compatible
formatting string \* time.locale: locale to use rather than the system
default

.. raw:: html

   <p />

.. raw:: html

   <p />

|time| \| \|timetz \|Displays the current date and time.Parameters: \*
time.format: strftime()-compatible formatting string \* time.locale:
locale to use rather than the system default \| \|title \|Displays
focused i3 window title.Requirements: \* i3ipcParameters: \* title.max :
Maximum character length for title before truncating. Defaults to 64. \*
title.placeholder : Placeholder text to be placed if title was
truncated. Defaults to ‘…’. \* title.scroll : Boolean flag for scrolling
title. Defaults to False

.. raw:: html

   <p />

.. raw:: html

   <p />

|title| \| \|todo \|Displays the number of todo items from a text
fileParameters: \* todo.file: File to read TODOs from (defaults to
~/Documents/todo.txt)

.. raw:: html

   <p />

.. raw:: html

   <p />

|todo| \| \|traffic \|Displays network IO for interfaces.Parameters: \*
traffic.exclude: Comma-separated list of interface prefixes to exclude
(defaults to ‘lo,virbr,docker,vboxnet,veth’) \* traffic.states:
Comma-separated list of states to show (prefix with ‘^’ to invert -
i.e. ^down -> show all devices that are not in state down) \*
traffic.showname: If set to False, hide network interface name (defaults
to True) \* traffic.format: Format string for download/upload speeds.
Defaults to ‘{:.2f}’ \* traffic.graphlen: Graph lenth in seconds.
Positive even integer. Each char shows 2 seconds. If set, enables
up/down traffic graphs

.. raw:: html

   <p />

.. raw:: html

   <p />

|traffic| \| \|twmn \|Toggle twmn notifications. \| \|uptime \|Displays
the system uptime.

.. raw:: html

   <p />

.. raw:: html

   <p />

|uptime| \| \|vault \|Copy passwords from a password store into the
clipboard (currently supports only ‘pass’)Many thanks to
[@bbernhard](https://github.com/bbernhard) for the idea!Parameters: \*
vault.duration: Duration until password is cleared from clipboard
(defaults to 30) \* vault.location: Location of the password store
(defaults to ~/.password-store) \* vault.offx: x-axis offset of popup
menu (defaults to 0) \* vault.offy: y-axis offset of popup menu
(defaults to 0)

.. raw:: html

   <p />

.. raw:: html

   <p />

|vault| \| \|vpn \|Displays the VPN profile that is currently in
use.Left click opens a popup menu that lists all available VPN profiles
and allows to establisha VPN connection using that
profile.Prerequisites: \* tk python library (usually python-tk or
python3-tk, depending on your distribution) \* nmcli needs to be
installed and configured properly. To quickly test, whether nmcli is
working correctly, type ‘nmcli -g NAME,TYPE,DEVICE con’ which lists all
the connection profiles that are configured. Make sure that your VPN
profile is in that list! e.g: to import a openvpn profile via nmcli:
sudo nmcli connection import type openvpn file
</path/to/your/openvpn/profile.ovpn> \| \|watson \|Displays the status
of watson (time-tracking tool)Requires the following executable: \*
watson \| \|weather \|Displays the temperature on the current location
based on the ipRequires the following python packages: \*
requestsParameters: \* weather.location: Set location, defaults to
‘auto’ for getting location automatically from a web service If set to a
comma-separated list, left-click and right-click can be used to rotate
the locations. Locations should be city names or city ids. \*
weather.unit: metric (default), kelvin, imperial \* weather.showcity: If
set to true, show location information, otherwise hide it (defaults to
true) \* weather.showminmax: If set to true, show the minimum and
maximum temperature, otherwise hide it (defaults to false) \*
weather.apikey: API key from http://api.openweathermap.org

.. raw:: html

   <p />

.. raw:: html

   <p />

|weather| \| \|xkcd \|Opens a random xkcd comic in the browser. \|
\|xrandr \|Shows a widget for each connected screen and allows the user
to enable/disable screens.Parameters: \* xrandr.overwrite_i3config: If
set to ‘true’, this module assembles a new i3 config every time a screen
is enabled or disabled by taking the file ‘~/.config/i3/config.template’
and appending a file ‘~/.config/i3/config.<screen name>’ for every
screen. \* xrandr.autoupdate: If set to ‘false’, does *not* invoke
xrandr automatically. Instead, the module will only refresh when
displays are enabled or disabled (defaults to true)Requires the
following python module: \* (optional) i3 - if present, the need for
updating the widget list is auto-detectedRequires the following
executable: \* xrandr

.. raw:: html

   <p />

.. raw:: html

   <p />

|xrandr| \| \|yubikey \|Shows yubikey informationRequires:
https://github.com/Yubico/python-yubicoThe output indicates that a
YubiKey is not connected or it displaysthe corresponding serial number.
\| \|zpool \|Displays info about zpools present on the systemParameters:
\* zpool.list: Comma-separated list of zpools to display info for. If
empty, info for all zpools is displayed. (Default: ’‘) \* zpool.format:
Format string, tags {name}, {used}, {left}, {size}, {percentfree},
{percentuse}, {status}, {shortstatus}, {fragpercent}, {deduppercent} are
supported. (Default:’{name} {used}/{size} ({percentfree}%)‘) \*
zpool.showio: Show also widgets detailing current read and write I/O
(Default: true) \* zpool.ioformat: Format string for I/O widget, tags
{ops} (operations per seconds) and {band} (bandwidth) are supported.
(Default:’{band}’) \* zpool.warnfree: Warn if free space is below this
percentage (Default: 10) \* zpool.sudo: Use sudo when calling the
``zpool`` binary. (Default: false)Option ``zpool.sudo`` is intended for
Linux users using zfsonlinux older than 0.7.0: In pre-0.7.0releases of
zfsonlinux regular users couldn’t invoke even informative commands such
as\ ``zpool list``. If this option is true, command ``zpool list`` is
invoked with sudo. If this optionis used, the following (or ekvivalent)
must be added to the
``sudoers(5)``:\ ``<br />\<username/ALL\> ALL = (root) NOPASSWD: /usr/bin/zpool list<br />``\ Be
aware of security implications of doing this!

.. raw:: html

   <p />

.. raw:: html

   <p />

|zpool| \|

.. |amixer| image:: ../screenshots/amixer.png
.. |battery| image:: ../screenshots/battery.png
.. |bluetooth| image:: ../screenshots/bluetooth.png
.. |brightness| image:: ../screenshots/brightness.png
.. |caffeine| image:: ../screenshots/caffeine.png
.. |cmus| image:: ../screenshots/cmus.png
.. |cpu| image:: ../screenshots/cpu.png
.. |currency| image:: ../screenshots/currency.png
.. |date| image:: ../screenshots/date.png
.. |datetime| image:: ../screenshots/datetime.png
.. |disk| image:: ../screenshots/disk.png
.. |dnf| image:: ../screenshots/dnf.png
.. |dunst| image:: ../screenshots/dunst.png
.. |getcrypto| image:: ../screenshots/getcrypto.png
.. |git| image:: ../screenshots/git.png
.. |github| image:: ../screenshots/github.png
.. |http_status| image:: ../screenshots/http_status.png
.. |indicator| image:: ../screenshots/indicator.png
.. |kernel| image:: ../screenshots/kernel.png
.. |layout| image:: ../screenshots/layout.png
.. |load| image:: ../screenshots/load.png
.. |memory| image:: ../screenshots/memory.png
.. |mpd| image:: ../screenshots/mpd.png
.. |nic| image:: ../screenshots/nic.png
.. |pacman| image:: ../screenshots/pacman.png
.. |ping| image:: ../screenshots/ping.png
.. |redshift| image:: ../screenshots/redshift.png
.. |sensors| image:: ../screenshots/sensors.png
.. |sensors2| image:: ../screenshots/sensors2.png
.. |shortcut| image:: ../screenshots/shortcut.png
.. |spacer| image:: ../screenshots/spacer.png
.. |spotify| image:: ../screenshots/spotify.png
.. |stock| image:: ../screenshots/stock.png
.. |taskwarrior| image:: ../screenshots/taskwarrior.png
.. |time| image:: ../screenshots/time.png
.. |title| image:: ../screenshots/title.png
.. |todo| image:: ../screenshots/todo.png
.. |traffic| image:: ../screenshots/traffic.png
.. |uptime| image:: ../screenshots/uptime.png
.. |vault| image:: ../screenshots/vault.png
.. |weather| image:: ../screenshots/weather.png
.. |xrandr| image:: ../screenshots/xrandr.png
.. |zpool| image:: ../screenshots/zpool.png
