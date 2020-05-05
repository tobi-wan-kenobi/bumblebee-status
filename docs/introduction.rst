Introduction
================

Installation
----------------

.. code-block::


   # from git (development snapshot)
   $ git clone git://github.com/tobi-wan-kenobi/bumblebee-status

   # from AUR:
   git clone https://aur.archlinux.org/bumblebee-status.git
   cd bumblebee-status
   makepkg -sicr

   # from PyPI (thanks @tony):
   # will install bumblebee-status into ~/.local/bin/bumblebee-status
   pip install --user bumblebee-status

Dependencies
------------

:doc:`development/module` lists the dependencies
(Python modules and external executables) for each module. If you are
not using a module, you don’t need the dependencies.

Usage
------------

Normal usage
~~~~~~~~~~~~

In your i3wm configuration, modify the *status_command* for your i3bar
like this:

.. code-block::

   bar {
       status_command <path to bumblebee-status/bumblebee-status> \
           -m <list of modules> \
           -p <list of module parameters> \
           -t <theme>
   }

You can retrieve a list of modules (and their parameters) and themes by
entering:

.. code-block::

   $ cd bumblebee-status
   $ ./bumblebee-status -l themes
   $ ./bumblebee-status -l modules

To change the update interval, use:

.. code-block::

   $ ./bumblebee-status -m <list of modules> -p interval=<interval in seconds>

The update interval can also be changed on a per-module basis, like
this:

.. code-block::

   $ ./bumblebee-status -m cpu memory -p cpu.interval=5s memory.interval=1m

All modules can be given “aliases” using ``<module name>:<alias>``, by
which they can be parametrized, for example:

.. code-block::

   $ ./bumblebee-status -m disk:root disk:home -p root.path=/ home.path=/home

As a simple example, this is what my i3 configuration looks like:

.. code-block::

   bar {
       font pango:Inconsolata 10
       position top
       tray_output none
       status_command ~/.i3/bumblebee-status/bumblebee-status -m nic disk:root \
           cpu memory battery date time pasink pasource dnf \
           -p root.path=/ time.format="%H:%M CW %V" date.format="%a, %b %d %Y" \
           -t solarized-powerline
   }

Restart i3wm and - that’s it!

