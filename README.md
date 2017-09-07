# bumblebee-status

[![Build Status](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status.svg?branch=master)](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status)
[![Code Climate](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/gpa.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![Test Coverage](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/coverage.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/coverage)
[![Issue Count](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/issue_count.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)

**Many, many thanks to all contributors! As of now, 21 of the modules are from various contributors (!), and only 16 from myself.**

bumblebee-status is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

Focus is on:
* Ease of use (no configuration files!)
* Theme support
* Extensibility (of course...)

One thing I like in particular: You can use the mouse wheel up/down to switch workspaces forward and back everywhere throughout the bar (unless you have mapped the mouse wheel buttons to another action for a widget, in which case this doesn't work while hovering that particular widget).

I hope you like it and appreciate any kind of feedback: Bug reports, Feature requests, etc. :)

Thanks a lot!

Supported Python versions: 2.7, 3.3, 3.4, 3.5, 3.6

Explicitly unsupported Python versions: 3.2 (missing unicode literals)

# Documentation
See [the wiki](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki) for documentation.

Other resources:

* A list of [available modules](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/Available-Modules)
* [How to write a theme](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/How-to-write-a-theme)
* [How to write a module](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki/How-to-write-a-module)

# Installation
```
$ git clone git://github.com/tobi-wan-kenobi/bumblebee-status
```

# Usage
## Normal usage
In your i3wm configuration, modify the *status_command* for your i3bar like this:

```
bar {
	status_command = <path to bumblebee-status/bumblebee-status> -m <list of modules> -p <list of module parameters> -t <theme>
}
```

You can retrieve a list of modules and themes by entering:
```
$ cd bumblebee-status
$ ./bumblebee-status -l themes
$ ./bumblebee-status -l modules
```

Any parameter you can specify with `-p <name>=<value>`, you can alternatively specify in `~/.bumblebee-status.conf` or `~/.config/bumblebee-status.conf`. This parameters act as a **fallback**, so values specified with `-p` have priority.

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

## Errors
If errors occur, you should see them in the i3bar itself. If that does not work, or you need more information for troubleshooting, you can activate a debug log using the `-d` or `--debug` switch:

```
$ ./bumblebee-status -d -m <list of modules>
```

This will create a file called `~/bumblebee-status-debug.log` by default. The file name can be changed by using the `-f` or `--logfile` option.

# Required Modules

Modules and commandline utilities are only required for modules, the core itself has no external dependencies at all.

* psutil (for the modules 'cpu', 'memory', 'traffic')
* netifaces (for the modules 'nic', 'traffic')
* requests (for the modules 'weather', 'github', 'getcrypto', 'stock')
* power (for the module 'battery')
* dbus (for the module 'spotify')

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

# Examples
Here are some screenshots for all themes that currently exist:

:exclamation: Some themes (all 'Powerline' themes) require [Font Awesome](http://fontawesome.io/) and a powerline-compatible font ([powerline-fonts](https://github.com/powerline/fonts), for example) to display all icons correctly.

Gruvbox Powerline (`-t gruvbox-powerline`) (contributed by [@paxy97](https://github.com/paxy97)):

![Gruvbox Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-gruvbox.png)

Solarized Powerline (`-t solarized-powerline`):

![Solarized Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-solarized.png)

Gruvbox (`-t gruvbox`):

![Gruvbox](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/gruvbox.png)

Solarized (`-t solarized`):

![Solarized](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/solarized.png)

Powerline (`-t powerline`):

![Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline.png)

Default (nothing or `-t default`):

![Default](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/default.png)
