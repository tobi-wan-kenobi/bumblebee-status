<img src="https://github.com/kellya/bumblebee-status-icon/blob/main/img/bumblebee_status_rtl.svg" width="50" style="display:inline-block">bumblebee-status
=====================================================

logo courtesy of [kellya](https://github.com/kellya) - thank you!

[![Documentation Status](https://readthedocs.org/projects/bumblebee-status/badge/?version=main)](https://bumblebee-status.readthedocs.io/en/main/?badge=main)
![Commits since release](https://img.shields.io/github/commits-since/tobi-wan-kenobi/bumblebee-status/latest)
![AUR version (release)](https://img.shields.io/aur/version/bumblebee-status)
![AUR version (git)](https://img.shields.io/aur/version/bumblebee-status-git)
![PyPI version](https://img.shields.io/pypi/v/bumblebee-status)
![Contributors](https://img.shields.io/github/contributors-anon/tobi-wan-kenobi/bumblebee-status)
[![Tests](https://github.com/tobi-wan-kenobi/bumblebee-status/actions/workflows/autotest.yml/badge.svg?branch=main)](https://github.com/tobi-wan-kenobi/bumblebee-status/actions/workflows/autotest.yml)

[![Code Climate](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/gpa.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![Test Coverage](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/coverage.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/coverage)
[![Issue Count](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status/badges/issue_count.svg)](https://codeclimate.com/github/tobi-wan-kenobi/bumblebee-status)
[![CodeQL](https://github.com/tobi-wan-kenobi/bumblebee-status/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/tobi-wan-kenobi/bumblebee-status/actions/workflows/codeql-analysis.yml)
![License](https://img.shields.io/github/license/tobi-wan-kenobi/bumblebee-status)

**Many, many thanks to all contributors! I am still amazed by and deeply grateful for how many PRs this project gets.**

[Click here for a list of available modules](https://bumblebee-status.readthedocs.io/en/main/modules.html)

![Solarized Powerline](screenshots/themes/powerline-solarized.png)

bumblebee-status is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

Focus is on:
* ease of use, sane defaults (no mandatory configuration file)
* [easy creation of custom themes](https://bumblebee-status.readthedocs.io/en/main/development/theme.html)
* [easy creation of custom modules](https://bumblebee-status.readthedocs.io/en/main/development/module.html)

I hope you like it and I appreciate any kind of feedback: bug reports, feature requests, etc. :)

Thanks a lot!

Required i3wm version: 4.12+ (in earlier versions, blocks won't have background colors)

Supported Python versions: 3.4, 3.5, 3.6, 3.7, 3.8, 3.9

Supported FontAwesome version: 4 (free version of 5 doesn't include some of the icons)

---
***NOTE***

The default branch for this project is `main`. If you are curious why: [ZDNet:github-master-alternative](https://www.zdnet.com/article/github-to-replace-master-with-alternative-term-to-avoid-slavery-references/)

---

Example usage:

```
bar {
	status_command <path>/bumblebee-status -m cpu memory battery time \
		pasink pasource -p time.format="%H:%M" -t solarized
}
```

# Documentation
See [the docs](https://bumblebee-status.readthedocs.io) for detailed documentation.

See [FAQ](https://bumblebee-status.readthedocs.io/en/main/FAQ.html) for. well, FAQs.

Other resources:

* A list of [available modules](https://bumblebee-status.readthedocs.io/en/main/modules.html)
* [How to write a module](https://bumblebee-status.readthedocs.io/en/main/development/module.html)
* [How to write a theme](https://bumblebee-status.readthedocs.io/en/main/development/theme.html)

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

There is also a SlackBuild available here: [slackbuilds:bumblebee-status](http://slackbuilds.org/repository/14.2/desktop/bumblebee-status/) - many thanks to [@Tonus1](https://github.com/Tonus1)!

An ebuild, for Gentoo Linux, is available on [gallifrey overlay](https://github.com/fedeliallalinea/gallifrey/tree/master/x11-misc/bumblebee-status). Instructions for adding the overlay can be found [here](https://github.com/fedeliallalinea/gallifrey/blob/master/README.md).

# Dependencies
[Available modules](https://bumblebee-status.readthedocs.io/en/main/modules.html) lists the dependencies (Python modules and external executables)
for each module. If you are not using a module, you don't need the dependencies.

Some themes (e.g. all ‘powerline’ themes) require Font Awesome http://fontawesome.io/ and a powerline-compatible font (powerline-fonts) https://github.com/powerline/fonts

# Usage
## Normal usage
In your i3wm configuration, modify the *status_command* for your i3bar like this:

```bash
bar {
	status_command <path to bumblebee-status/bumblebee-status> \
		-m <list of modules> \
		-p <list of module parameters> \
		-t <theme>
}
```

You can retrieve a list of modules (and their parameters) and themes by entering:
```bash
$ cd bumblebee-status
$ ./bumblebee-status -l themes
$ ./bumblebee-status -l modules
```

To change the update interval, use:
```bash
$ ./bumblebee-status -m <list of modules> -p interval=<interval in seconds>
```

The update interval can also be changed on a per-module basis, like this:
```bash
$ ./bumblebee-status -m cpu memory -p cpu.interval=5s memory.interval=1m
```

All modules can be given "aliases" using `<module name>:<alias>`, by which they can be parametrized, for example:

```bash
$ ./bumblebee-status -m disk:root disk:home -p root.path=/ home.path=/home
```

As a simple example, this is what my i3 configuration looks like:

```bash
bar {
	font pango:Inconsolata 10
	position top
	tray_output none
	status_command ~/.i3/bumblebee-status/bumblebee-status -m nic disk:root cpu \
		memory battery date time pasink pasource dnf \
		-p root.path=/ time.format="%H:%M CW %V" date.format="%a, %b %d %Y" \
		-t solarized-powerline
}

```

Restart i3wm and - that's it!

# Examples

[List of themes](https://bumblebee-status.readthedocs.io/en/main/themes.html)
