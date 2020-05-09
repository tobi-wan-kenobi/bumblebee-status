How to write a new module
=========================

Introduction
------------

Adding a new module to ``bumblebee-status`` is straight-forward:

-  Add a new Python module in ``modules/contrib/``. The name of the
   module will be the name that the user needs to specify when invoking
   ``bumblebee-status`` (i.e. a module called
   ``modules/contrib/test.py`` will be loaded using
   ``bumblebee-status -m test``)
-  See below for how to actually write the module
-  Test (run ``bumblebee-status`` in the CLI)
-  Make sure your changes don’t break anything: ``./coverage.sh``
-  If you want to do me favour, run your module through
   ``black -t py34`` before submitting

Pull requests
-------------

The project **gladly** accepts PRs for bugfixes, new functionality, new
modules, etc. When you feel comfortable with what you’ve developed,
please just open a PR, somebody will look at it eventually :) Thanks!

Coding guidelines
-----------------

I’m pretty open to whatever style you use, but if it’s all the same to
you (and yes, I know that the current codebase is only slowly adapting
to this): - Please favour single quotes for strings (except for
docstrings, which are always """) - For private methods/variables,
please use a leading ``__`` (e.g. ``__output`` rather than ``_output``)

Hello world
-----------

This example will show “hello world” in the status bar:

.. code:: python

   """Short description in RST format

      please have a look at other modules, this will go into the
      documentation verbatim (list of modules)
   """

   import core.module
   import core.widget

   class Module(core.module.Module):
       def __init__(self, config):
           super().__init__(config, core.widget.Widget(self.full_text))

       def full_text(self, widgets):
           return 'hello world'

   # vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

Of modules and widgets
----------------------

There are two important concepts for module writers: - A module is
something that offers a single set of coherent functionality - A module
has 1 to n “widgets”, which translates to individual blocks in the i3bar

Very often, this is a 1:1 relationship, and a single module has a single
widget. If that’s the case for you, you can stop reading now :)

Otherwise, you have a number of ways to handle widgets: - During the
``super().init__(...)`` inside the module’s constructor, you can specify
a **list** of widgets, and those will comprise the widgets (in ordered
fashion) - During runtime, you can set a new list of widgets by using
the ``self.add_widget()`` method of the module to add new widgets and
``self.clear_widgets()`` method to remove all widgets.

Adding widgets at runtime
-------------------------

If you want to add widgets during runtime, please use the
``add_widget()`` method of the module:

::

   def do_something(self):
       self.add_widget(full_text="my sample text", name="<optional name>")

TODO: expand on this

Periodic updates
----------------

``bumblebee-status`` modules have two different ways to update their
data: 1. Each interval, the callback registered when the widget was
created is called. You can do arbitrarily complex things there 2. Each
interval, **before** the widget’s callback is invoked, a generic
``update(self, widgets)`` method is called on the **module**

Largely, where you want to put your update code is up to you. My
observations: - If you want to change the widgets a module has, you
**have** to stick with ``update()`` - For simple modules, doing the data
update in the widget callback is simplest (see ``kernel``, for example)

Advanced topics
---------------

Event handlers
~~~~~~~~~~~~~~

The ``core.input`` module can be used to execute callbacks during mouse
events:

.. code:: python

   import core.module
   import core.widget
   import core.input

   class Module(core.module.Module):
       @core.decorators.every(minutes=60, seconds=20)
       def __init__(self, config):
           super().__init__(config=config, widgets=<widgets>)

           core.input.register(widget, button=core.input.LEFT_MOUSE, cmd=<cmd>)

The command can be either a CLI tool that will be directly executed
(e.g. ``cmd='shutdown -h now'``) or a method that will be executed. The
method’s signature needs to be: ``def <name>(self, event)``, where
“event” is the event data provided by i3wm.

The full list of possible bindings: - LEFT_MOUSE - RIGHT_MOUSE -
MIDDLE_MOUSE - WHEEL_UP - WHEEL_UP

Setting a default update interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To change the default update interval, you can use a simple decorator:

.. code:: python

   import core.module
   import core.widget
   import core.decorators

   class Module(core.module.Module):
       @core.decorators.every(minutes=60, seconds=20)
       def __init__(self, config):
           super().__init__(config=config, widgets=<widgets>)

**NOTE**: This makes the update interval of the module independent of
what the user configures via ``-i <interval>``! It is still possible to
override the module’s interval using ``-p <module>.interval=<value>``,
however.

TODOs
-----

-  default update interval
-  scrolling
-  theme.minwidth
-  scrolling decorator
-  theme.exclude
-  per module update interval -> nice string format
-  update via events
