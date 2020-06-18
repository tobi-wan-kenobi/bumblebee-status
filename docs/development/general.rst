General guidelines
==================

Writing unit tests
------------------

Some general hints:

- Tests should run with just Python Standard Library modules installed
  (i.e. if there are additional requirements, the test should be skipped
  if those are missing)
- Tests should run even if there is no network connectivity (please mock
  urllib calls, for example)
- Tests should be stable and not require modifications every time the
  tested code's implementation changes slightly (been there / done that)

Right now, ``bumblebee-status`` is moving away from Python's
built-in ``unittest`` framework (tests located inside ``tests/``)
and towards ``pytest`` (tests located inside ``pytests/``).

First implication: To run the new tests, you need to have ``pytest``
installed, it is not part of the Python Standard Library. Most
distributions call the package ``python-pytest`` or ``python3-pytest``
or something similar (or you just use ``pip install --use pytest``)

Aside from that, you just write you tests using ``pytest`` as usual,
with one big caveat:

**If** you create a new directory inside ``pytests/``, you need to
also create a file called ``__init__.py`` inside that, otherwise,
modules won't load correctly.

For examples, just browse the existing code. A good, minimal sample
for unit testing ``bumblebee-status`` is ``pytests/core/test_event.py``.
