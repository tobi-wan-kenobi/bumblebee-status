# bumblebee-status

[![Build Status](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status.svg?branch=master)](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status)
[![Code Climate](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/gpa.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![Test Coverage](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/coverage.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/coverage)
[![Issue Count](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/issue_count.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)

**Many, many thanks to all contributors! All of the really cool modules have been contributed by somebody :)**

![List of modules](doc/MODULES.md)

![Solarized Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-solarized.png)

bumblebee-status is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

Focus is on:
* Ease of use
* Support for easily adding custom themes
* Support for easily adding custom modules

I hope you like it and I appreciate any kind of feedback: Bug reports, Feature requests, etc. :)

Thanks a lot!

Required i3wm version: 4.12+ (in earlier versions, blocks won't have background colors)

Supported Python versions: 3.4, 3.5, 3.6, 3.7, 3.8

Supported FontAwesome version: 4 (free version of 5 doesn't include some of the icons)

Example usage:

```
bar {
	status_command <path>/bumblebee-status -m cpu memory battery time pasink pasource -p time.format="%H:%M" -t solarized
}
```

# Documentation
See [the wiki](https://github.com/tobi-wan-kenobi/bumblebee-status/wiki) for documentation.

See [FAQ](doc/FAQ.md) for FAQs.

Other resources:

* A list of [available modules](doc/MODULES.md)
* [How to write a theme](doc/HOWTO_THEME.md)
* [How to write a module](doc/HOWTO_MODULE.md)

# Installation
```
$ git clone git://github.com/tobi-wan-kenobi/bumblebee-status
```

# Dependencies
[Available modules](doc/MODULES.md) lists the dependencies (Python modules and external executables)
for each module. If you are not using a module, you don't need the dependencies.

# Usage
## Normal usage
In your i3wm configuration, modify the *status_command* for your i3bar like this:

```
bar {
	status_command <path to bumblebee-status/bumblebee-status> \
		-m <list of modules> \
		-p <list of module parameters> \
		-t <theme>
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

This will log to stderr, so unless you are running `bumblebee-status` interactively in the CLI, you'll need to redirect stderr to some file (i.e. `bumblebee-status <parameters> 2> error.log`).

### Advanced Usage
If you want to have a minimal bar that stays out of the way, you can use the `-a` or `--autohide` switch to specify a list of module names. All those modules will only be displayed when (and as long as) their state is either warning or critical (high CPU usage, low disk space, etc.). As long as the module is in a "normal" state and does not require attention, it will remain hidden.
Note that this parameter is specified *in addition* to `-m` (i.e. to autohide the CPU module, you would use `bumblebee-status -m cpu memory traffic -a cpu`).

# Examples

![List of themes](./doc/THEMES.md)
