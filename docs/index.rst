.. bumblebee-status documentation master file, created by
   sphinx-quickstart on Mon May  4 08:03:26 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bumblebee-status's documentation!
============================================

bumblebee-status is a modular, theme-able status line generator for the
`i3 window manager <https://i3wm.org/>`__.

Logo courtesy of [kellya](https://github.com/kellya) - thank you!

Focus is on:

 - ease of use, sane defaults (no mandatory configuration file)
 - custom modules: :doc:`development/module`
 - custom themes: :doc:`development/theme`
 
I hope you like it and I appreciate any kind of feedback: bug reports,
feature requests, etc. :)

Thanks a lot!

+------------------------------------+------------------------------+
| **Required i3wm version**          | 4.12+                        |
+------------------------------------+------------------------------+
| **Supported Python versions**      | 3.4, 3.5, 3.6, 3.7, 3.8, 3.9 |
+------------------------------------+------------------------------+
| **Supported FontAwesome versions** | 4 only                       |
+------------------------------------+------------------------------+
| **Per-module requirements**        | see :doc:`modules`           |
+------------------------------------+------------------------------+

see :doc:`FAQ` for details on this

Example usage:

.. code-block:: bash

   bar {
       status_command <path>/bumblebee-status \
        -m cpu memory battery time pasink pasource \
        -p time.format="%H:%M" \
        -t solarized
   }

.. toctree::
   :maxdepth: 2
   :caption: Contents

   introduction
   features
   FAQ
   modules
   themes
   development/index

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
