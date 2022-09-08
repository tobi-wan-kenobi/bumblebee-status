How to write a module
=====================

Introduction
------------

Adding a new module to ``bumblebee-status`` is straight-forward:

-  Add a new Python module in ``bumblebee_status/modules/contrib/``. The name of the
   module will be the name that the user needs to specify when invoking
   ``bumblebee-status`` (i.e. a module called
   ``bumblebee_status/modules/contrib/test.py`` will be loaded using
   ``bumblebee-status -m test``)
-  Alternatively, you can put your module in ``~/.config/bumblebee-status/modules/``
-  The module name must follow the `Python Naming Conventions <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_
-  See below for how to actually write the module
-  Test (run ``bumblebee-status`` in the CLI)
-  Make sure your changes don’t break anything: ``./coverage.sh``
-  If you want to do me a favour, run your module through
   ``black -t py34`` before submitting

Pull requests
-------------

The project **gladly** accepts PRs for bugfixes, new functionality, new
modules, etc. When you feel comfortable with what you’ve developed,
please just open a PR. Somebody will look at it eventually :) Thanks!

Coding guidelines
-----------------

I’m pretty open to whatever style you use, but if it’s all the same to
you (and yes, I know that the current codebase is only slowly adapting
to this): - Please favour double quotes for strings.
For private methods/variables,
please use a leading ``__`` (e.g. ``__output`` rather than ``_output``)

For anything else, please run your code through `black <https://github.com/psf/black>`_.

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
has 1 to n “widgets”, which translates to individual blocks in the i3bar.

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

Periodic updates (update() vs. full_text)
-----------------------------------------

``bumblebee-status`` modules have two different ways to update their
data: 1. Each interval, the callback registered when the widget was
created is called. You can do arbitrarily complex things there 2. Each
interval, **before** the widget’s callback is invoked, a generic
``update(self, widgets)`` method is called on the **module**

Largely, where you want to put your update code is up to you. My
observations: - If you want to change the widgets a module has, you
**have** to stick with ``update()`` - For simple modules, doing the data
update in the widget callback is simplest (see ``kernel``, for example)

Widget states
-------------

Each widget inside a module can have a list of states (for example, two
predefined states are ``warning`` and ``critical``). States define how
a widget is rendered (i.e. which fields in the theme file are selected to
draw it.

Somewhat paradoxically, to give a **widget** a state, a method called
``def state(self, widget)`` has to be defined on the **module**. The
reason for this is that the module typically contains all of the statefulness,
so assumedly, it's easier to determine the state of a widget from the
module, rather than from the widget itself.

The ``state()`` method simply returns a list of strings, which make up
the state this particular widget has.

The themeing code then iterates these states and selects the matching
theme information from the theme file. This, it does by performing a "best match"
search through the theme, like this:

- Is there a theme definition for the **module** that in turn contains a JSON object
  for the **state**? If so, use that (for example: ``"cpu": { "critical": { "fg": "#ff0000" } }``)
- If not, is there a theme definition inside the ``defaults`` or ``cycle`` theme entries?

For more details on that, please refer to `How to write a theme <theme.rst>`_

If multiple states match on the "same level", the last state in the state list is used.
For example, if a module returns ``[ "critical", "warning" ]`` as state, typically, the
widget will be drawn as ``warning``.

One important helper method is ``def threshold_state(value, warning, critical)``, which each
module possesses. Using that, it is very easy to define warning and critical states when the
widget represents a simple numeric value.

Sounds confusing? An example will clarify: Let's say your widget returns a percentage (disk
usage, or CPU usage). The widget should be marked as "warning" when the percentage is above
50, and as "critical", if it is above 90. This, you would do like this:

.. code-block:: python

  def state(self, widget):
      return self.threshold_state(self.__value, 50, 90)


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

Redraw outside the update interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, it is desirable to redraw a widget dynamically, even outside its update
interva. This can be useful if the value to be displayed is calculated in a separate
thread. In such a scenario, the ``update()`` method would simply trigger of a thread
and the actual value would be available later (but presumably before the next
update call).

If that is the case, it is possible to fire off an event in the thread to cause the
affected widget to be redrawn, like this:

.. code:: python

    import core.event

    # later
    core.event.trigger("update", [<list of module IDs>], redraw_only=True)

A concrete example of this can be found in the module ``redshift``, and a couple of others.

Scrolling content
~~~~~~~~~~~~~~~~~

If a widgets produces a large amount of content, it might be desirable to limit the amount
of space the widget can occupy and scroll the content, if necessary.

This behaviour can be achieved using the ``scrollable`` decorator like this:

.. code:: python

    import core.module
    import core.widget
    import core.decorators

    class Module(core.module.Module):
        def __init__(self, config, theme):
            super().__init__(config, theme, core.widget.Widget(self.description))

    @core.decorators.scrollable
    def description(self, widget):
        pass # TODO: implement

There are a couple of parameters that can be set on the affected module, either in the
module using ``self.set()`` or via the CLI using the ``--parameter`` flag:

- ``scrolling.width``: Integer, defaults to 30, determines the minimum width of the widgets, if ``makewide`` is specified
- ``scrolling.makewide``: Boolean, defaults to true,  determines whether the widgets should be expanded to their minwidth
- ``scrolling.bounce``: Boolean, defaults to true, determines whether the content should change directions when a scroll is completed, or just marquee through

