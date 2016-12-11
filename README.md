# bumblebee-status

[![Build Status](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status.svg?branch=master)](https://travis-ci.org/tobi-wan-kenobi/bumblebee-status)
[![Code Climate](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/gpa.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![Test Coverage](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/coverage.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/coverage)
[![Issue Count](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/issue_count.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)

bumblebee-status is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

Focus is on:
* Ease of use (no configuration files!)
* Theme support
* Extensibility (of course...)

I hope you like it and appreciate any kind of feedback: Bug reports, Feature requests, etc. :)

Thanks a lot!

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

Next, open your i3wm configuration and modify the *status_command* for your i3bar like this:

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
Here are some screenshots for all themes that currently exist:

Gruvbox Powerline (`-t gruvbox-powerline`) (contributed by [@paxy97](https://github.com/paxy97)):

![Gruvbox Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-gruvbox.png)

Solarized Powerline (`-t solarized-powerline`):

![Solarized Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline-solarized.png)

Solarized (`-t solarized`):

![Solarized](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/solarized.png)

Powerline (`-t powerline`):

![Powerline](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/powerline.png)

Default (nothing or `-t default`):

![Default](https://github.com/tobi-wan-kenobi/bumblebee-status/blob/master/screenshots/themes/default.png)
