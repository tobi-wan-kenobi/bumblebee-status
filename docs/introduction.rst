Introduction
================

Installation
----------------

.. code-block:: bash


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

:doc:`modules` lists the dependencies
(Python modules and external executables) for each module. If you are
not using a module, you don’t need the dependencies.

Usage
------------

In your i3wm configuration, modify the *status_command* for your i3bar
like this:

.. code-block:: bash

   bar {
       status_command <path to bumblebee-status/bumblebee-status> \
           -m <list of modules> \
           -p <list of module parameters> \
           -t <theme>
   }

You can retrieve a list of modules (and their parameters) and themes by
entering:

.. code-block:: bash

   $ cd bumblebee-status
   $ ./bumblebee-status -l themes
   $ ./bumblebee-status -l modules

To change the update interval, use:

.. code-block:: bash

   $ ./bumblebee-status -m <list of modules> -p interval=<interval in seconds>

Note that some modules define their own intervals (e.g. most modules that query
an online service), such as to not cause a storm of "once every second" queries.

For such modules, the "global" interval defined here effectively defines the
highest possible "resolution". If you have a global interval of 10s, for example,
any other module can update at 10s, 20s, 30s, etc., but not every 25s. The status
bar will internally always align to the next future time slot.

The update interval can also be changed on a per-module basis, like
this (overriding the default module interval indicated above):

.. code-block:: bash

   $ ./bumblebee-status -m cpu memory -p cpu.interval=5s memory.interval=1m

All modules can be given “aliases” using ``<module name>:<alias>``, by
which they can be parametrized, for example:

.. code-block:: bash

   $ ./bumblebee-status -m disk:root disk:home -p root.path=/ home.path=/home

As a simple example, this is what my i3 configuration looks like:

.. code-block:: bash

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

