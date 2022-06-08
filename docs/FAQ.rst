.. contents::

FAQs
====

The new version has broken my setup!
-----------------------------------------

First, sorry about that!

Then, please open a bug report and I will try to fix the issue quickly.

If that is not an acceptable solution, here are different ways to step
back to the last stable version:

git
  ``git checkout v1.10.4``
pip
  ``pip install --user --force-reinstall bumblebee-status==1.10.4``
aur
  ``# checkout rev. 7ac3dde7361c6a530141df2b3c0137f57d6b4f70 from https://aur.archlinux.org/bumblebee-status.git``

My bar doesn’t show any background colors
-----------------------------------------

Please check that you are using i3wm 4.12 or later. Before that, i3wm
didn’t have background color support for the status bar.

Some of the icons don’t render correctly
----------------------------------------

Please check that you have `Font Awesome`_ installed (version 4).

.. note:: The `Font Awesome`_ is required for all themes that
    contain icons (because that is the font that includes these icons).
    Please refer to your distribution’s package management on how to install
    them, or get them from their website directly. Also, please note that
    Font Awesome removed some icons used by ``bumblebee-status`` from the
    free set in version 5, so if possible, stick with 4.

.. code-block:: bash

   # Font Awesome installation instructions

   # Arch Linux
   $ sudo pacman -S awesome-terminal-fonts

   # FreeBSD
   $ sudo pkg install font-awesome
   $ sudo pkg install py36-tzlocal py36-pytz py36-netifaces py36-psutil py36-requests #for dependencies

   # Other
   # see https://github.com/gabrielelana/awesome-terminal-fonts

You might also need to add it to the `font` directive in your i3 configuration, for example:

.. code-block::

    bar {
        font pango:FontAwesome, Fira mono 10
        status_command bumblebee-status -m title pasink pasource cpu memory battery datetime --iconset awesome-fonts
    }

If you are unsure about how the font is named, you can use the ``pango-list`` command line tool to look at the fonts installed on your computer. Also note how you can specify multiple fonts, separated by commas, in the above example.

.. _Font Awesome: https://fontawesome.com/
