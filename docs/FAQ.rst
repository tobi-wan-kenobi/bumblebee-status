.. contents::

FAQs
====

My bar doesn’t show any background colors
-----------------------------------------

Please check that you are using i3wm 4.12 or later. Before that, i3wm
didn’t have background color support for the status bar.

Some of the icons don’t render correctly
----------------------------------------

Please check that you have |Font Awesome| installed (version 4).

.. note:: The |Font Awesome| is required for all themes that
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

.. |Font Awesome| image:: https://fontawesome.com/
