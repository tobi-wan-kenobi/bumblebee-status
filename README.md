# bumblebee-status

[![Build Status](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status.svg?branch=master)](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status)
[![Code Climate](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/gpa.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![Test Coverage](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/coverage.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/coverage)
[![Issue Count](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/issue_count.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)

**Many, many thanks to all contributors! All of the really cool modules have been contributed by somebody else :)**

![List of modules](doc/LIST-OF-MODULES.md)

![Solarized Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-solarized.png)

bumblebee-status is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

Focus is on:
* Ease of use
* Support for easily adding [custom themes](doc/development/WRITING-A-THEME.md)
* Support for easily adding [custom modules](doc/development/WRITING-A-MODULE.md)

I hope you like it and I appreciate any kind of feedback: Bug reports, feature requests, etc. :)

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
See [the docs](doc/) for documentation.

See [FAQ](doc/FAQ.md) for FAQs.

Other resources:

* A list of [available modules](doc/LIST-OF-MODULES.md)
* [How to write a module](doc/development/WRITING-A-MODULE.md)
* [How to write a theme](doc/development/WRITING-A-THEME.md)

# Installation
```
# from git (development snapshot)
$ git clone git://github.com/tobi-wan-kenobi/bumblebee-status

# from AUR:
git clone https://aur.archlinux.org/bumblebee-status.git
cd bumblebee-status
makepkg -sicr

# from PyPI (thanks @tony):
# will install bumblebee-status into ~/.local/bin/bumblebee-status
pip install --user bumblebee-status
```

# Dependencies
[Available modules](doc/LIST-OF-MODULES.md) lists the dependencies (Python modules and external executables)
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

The update interval can also be changed on a per-module basis, like this:
```
$ ./bumblebee-status -m cpu memory -p cpu.interval=5s memory.interval=1m
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

# Examples

![List of themes](./doc/LIST-OF-THEMES.md)
