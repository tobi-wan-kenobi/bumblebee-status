# bumblebee-status

[![Build Status](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status.svg?branch=master)](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status)
[![Code Climate](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/gpa.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![Test Coverage](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/coverage.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/coverage)
[![Issue Count](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/issue_count.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)

**Many, many thanks to all contributors! As of now, 39 of the modules are from various contributors (!), and only 18 from myself.**

![Solarized Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-solarized.png)

bumblebee-status is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

Focus is on:
* Ease of use (no configuration files!)
* Theme support
* Extensibility (of course...)

One thing I like in particular: You can use the mouse wheel up/down to switch workspaces forward and back everywhere throughout the bar (unless you have mapped the mouse wheel buttons to another action for a widget, in which case this doesn't work while hovering that particular widget).

I hope you like it and appreciate any kind of feedback: Bug reports, Feature requests, etc. :)

Thanks a lot!

Required i3wm version: 4.12+ (in earlier versions, blocks won't have background colors)

Supported Python versions: 2.7, 3.3, 3.4, 3.5, 3.6

Supported FontAwesome version: 4 (free version of 5 doesn't include some of the icons)

Explicitly unsupported Python versions: 3.2 (missing unicode literals)

:information_source: The ![Font Awesome](https://fontawesome.com/) is required for all themes that contain icons (because that is the font that includes these icons). Please refer to your distribution's package management on how to install them, or get them from their website directly. Also, please note that Font Awesome removed some icons used by `bumblebee-status` from the free set in version 5, so if possible, stick with 4.

```
# Font Awesome installation instructions

# Arch Linux
$ sudo pacman -S awesome-terminal-fonts

# Other
# see https://github.com/gabrielelana/awesome-terminal-fonts
```

Example usage:

```
bar {
	status_command <path>/bumblebee-status -m cpu memory battery time pasink pasource -p time.format="%H:%M" -t solarized
}
```

# Documentation
See [the wiki](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki) for documentation.

See [FAQ](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/FAQ) for, well, FAQs.

Other resources:

* A list of [available modules](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/Available-Modules)
* [How to write a theme](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/How-to-write-a-theme)
* [How to write a module](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/How-to-write-a-module)

# Installation
```
$ git clone git://github.com/tobi-wan-kenobi/bumblebee-status
```

# Dependencies
[Available modules](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/Available-Modules) lists the dependencies (Python modules and external executables)
for each module. If you are not using a module, you don't need the dependencies.

# Usage
## Normal usage
In your i3wm configuration, modify the *status_command* for your i3bar like this:

```
bar {
	status_command <path to bumblebee-status/bumblebee-status> -m <list of modules> -p <list of module parameters> -t <theme>
}
```

You can retrieve a list of modules (and their parameters) and themes by entering:
```
$ cd bumblebee-status
$ ./bumblebee-status -l themes
$ ./bumblebee-status -l modules
```

Any parameter you can specify with `-p <name>=<value>`, you can alternatively specify in `~/.bumblebee-status.conf` or `~/.config/bumblebee-status.conf`. This parameters act as a **fallback**, so values specified with `-p` have priority.

Parameters can also be used to override theme settings, such as:

```
$ ./bumblebee-status -p <module>.theme.<theme field>=<value>
# for example, to get a spacer with a red background:
$ ./bumblebee-status -m spacer -p spacer.theme.bg=#ff0000
```

Configuration files have a format like this:
```
$ cat ~/.bumblebee-status.conf
[module-parameters]
<key> = <value>
```

For example:
```
$ cat ~/.bumblebee-status.conf
[module-parameters]
github.token=abcdefabcdef12345
```

To change the update interval, use:
```
$ ./bumblebee-status -m <list of modules> -p interval=<interval in seconds>
```

As a simple example, this is what my i3 configuration looks like:

```
bar {
	font pango:Inconsolata 10
	position top
	tray_output none
	status_command ~/.i3/bumblebee-status/bumblebee-status -m nic disk:root cpu memory battery date time pasink pasource dnf -p root.path=/ time.format="%H:%M CW %V" date.format="%a, %b %d %Y" -t solarized-powerline
}

```

Restart i3wm and - that's it!

## Events
By default, the following events are handled:

- Mouse-Wheel on any module moves to the next/previous i3 workspace
- Left-click on the "disk" module opens the specified path in nautilus
- Left-click on either "memory" or "cpu" opens gnome-system-monitor
- Left-click on a "pulseaudio" (or pasource/pasink) module toggles the mute state
- Right-click on a "pulseaudio" module opens pavucontrol
- Mouse-Wheel up/down on a "pulseaudio" module raises/lowers the volume

By default, the Mouse-Wheel wraps for the current output. You can disable this behavior by providing the parameter `engine.workspacewrap=false` (starting with version 1.4.5). Also, you can completely disable output switching by using `engine.workspacewheel=false`.

You can provide your own handlers to any module by using the following "special" configuration parameters:

- left-click
- right-click
- middle-click
- wheel-up
- wheel-down
For example, to execute "pavucontrol" whenever you left-click on the nic module, you could write:

`$ bumblebee-status -p nic.left-click="pavucontrol"`

In the string, you can use the following format identifiers:
- name
- instance
- button

For example:

`$ bumblebee-status -p disk.left-click="nautilus {instance}"`

## Errors
If errors occur, you should see them in the i3bar itself. If that does not work, or you need more information for troubleshooting, you can activate a debug log using the `-d` or `--debug` switch:

```
$ ./bumblebee-status -d -m <list of modules>
```

This will create a file called `~/bumblebee-status-debug.log` by default. The file name can be changed by using the `-f` or `--logfile` option.

### Advanced Usage
If you want to have a minimal bar that stays out of the way, you can use the `-a` or `--autohide` switch to specify a list of module names. All those modules will only be displayed when (and as long as) their state is either warning or critical (high CPU usage, low disk space, etc.). As long as the module is in a "normal" state and does not require attention, it will remain hidden.

# Required Modules

Modules and commandline utilities are only required for modules, the core itself has no external dependencies at all.

* psutil (for the modules 'cpu', 'memory', 'traffic')
* netifaces (for the modules 'nic', 'traffic')
* requests (for the modules 'weather', 'github', 'getcrypto', 'stock', 'currency')
* power (for the module 'battery')
* dbus (for the module 'spotify')
* i3ipc (for the module 'title')
* pacman-contrib (for module 'arch-update')
* docker (for the module 'docker_ps')

# Required commandline utilities

* xset (for the module 'caffeine')
* notify-send (for the module 'caffeine')
* cmus-remote (for the module 'cmus')
* dnf (for the module 'dnf')
* gpmdp-remote (for the module 'gpmdp')
* setxkbmap (for the module 'layout')
* fakeroot (for the module 'pacman')
* pacman (for the module 'pacman')
* pactl (for the module 'pulseaudio')
* ping (for the module 'ping')
* redshift (for the module 'redshift')
* xrandr (for the module 'xrandr')
* mpc (for the module 'mpd')
* bluez / blueman (for module 'bluetooth')
* dbus-send (for module 'bluetooth')
* nvidia-smi (for module 'nvidiagpu')
* sensors (for module 'sensors', as fallback)
* zpool (for module 'zpool')
* progress (for module 'progress')

# Examples
Here are some screenshots for all themes that currently exist:

:exclamation: Some themes (all 'Powerline' themes) require [Font Awesome](http://fontawesome.io/) and a powerline-compatible font ([powerline-fonts](https://github.com/powerline/fonts), for example) to display all icons correctly.

Gruvbox Powerline (`-t gruvbox-powerline`) (contributed by [@TheEdgeOfRage](https://github.com/TheEdgeOfRage)):

![Gruvbox Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-gruvbox.png)

Gruvbox Powerline Light (`-t gruvbox-powerline-light`) (contributed by [freed00m](https://github.com/freed00m)):

![Gruvbox Powerline Light](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/gruvbox-powerline-light.png)

Solarized Powerline (`-t solarized-powerline`):

![Solarized Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-solarized.png)

Gruvbox (`-t gruvbox`):

![Gruvbox](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/gruvbox.png)

Gruvbox Light (`-t gruvbox-light`) (contributed by [freed00m](https://github.com/freed00m)):

![Gruvbox Light](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/gruvbox-light.png)

Solarized (`-t solarized`):

![Solarized](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/solarized.png)

Powerline (`-t powerline`):

![Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline.png)

Greyish Powerline (`-t greyish-powerline`) (contributed by Joshua Bark):

![Greyish Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-greyish.png)

Iceberg (`-t iceberg`) (contributed by [whzup](https://github.com/whzup)):

![Iceberg](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/iceberg.png)

Iceberg Powerline (`-t iceberg-powerline`) (contributed by [whzup](https://github.com/whzup)):

![Iceberg Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/iceberg-powerline.png)

Iceberg Dark Powerline (`-t iceberg-dark-powerline`) (contributed by [gkeep](https://github.com/gkeep)):

![Iceberg Dark Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/iceberg-dark-powerline.png)

Iceberg Rainbow (`-t iceberg-rainbow`) (contributed by [whzup](https://github.com/whzup)):

![Iceberg Rainbow](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/iceberg-rainbow.png)

One Dark Powerline (`-t onedark-powerline`) (contributed by [dillasyx](https://github.com/dillasyx)):

![One Dark Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/onedark-powerline.png)

Default (nothing or `-t default`):

![Default](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/default.png)
