# i3bumblebee

i3bumblebee is a modular, theme-able status line generator for the [i3 window manager](https://i3wm.org/).

# Documentation
See [the wiki](https://github.com/tobi-wan-kenobi/i3bumblebee/wiki) for documentation.

Other resources:

* A list of [available modules](https://github.com/tobi-wan-kenobi/i3bumblebee/wiki/Available-Modules)
* [How to write a theme](https://github.com/tobi-wan-kenobi/i3bumblebee/wiki/How-to-write-a-theme)
* [How to write a module](https://github.com/tobi-wan-kenobi/i3bumblebee/wiki/How-to-write-a-module)

# Installation
```
$ git clone git://github.com/tobi-wan-kenobi/i3bumblebee
```

# Usage

Next, open your i3wm configuration and modify the *status_command* for your i3bar like this:

```
bar {
	status_command = <path to i3bumblebee/i3bumblebee> -m <list of modules> -t <theme>
}
```

You can retrieve a list of modules and themes by entering:
```
$ cd i3bumblebee
$ ./i3bumblebee -l
```

As a simple example, this is what my i3 configuration looks like:

```
bar {
	font pango:Inconsolata 10
	position top
	tray_output none
	status_command ~/src/i3bumblebee/i3bumblebee -m disk disk::/home nic cpu memory battery date::"%a, %b %d %Y" spacer time::"%H:%M CW %V" pasink pasource dnf -t solarized-powerline
}

```


Restart i3wm and - that's it!


# Examples
Here are some screenshots for all themes that currently exist:

Solarized Powerline (`-t solarized-powerline`):
![Solarized Powerline](https://github.com/tobi-wan-kenobi/i3bumblebee/blob/master/screenshots/powerline-solarized.png)

Solarized (`-t solarized`):
![Solarized](https://github.com/tobi-wan-kenobi/i3bumblebee/blob/master/screenshots/solarized.png)

Powerline (`-t powerline`):
![Powerline](https://github.com/tobi-wan-kenobi/i3bumblebee/blob/master/screenshots/powerline.png)

Default (nothing or `-t default`):
![Default](https://github.com/tobi-wan-kenobi/i3bumblebee/blob/master/screenshots/default.png)
