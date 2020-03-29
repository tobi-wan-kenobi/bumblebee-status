# Writing a bumblebee-status module

## Introduction
Adding a new module to `bumblebee-status` is straight-forward:

- Add a new Python module in `modules/contrib/`. The name of the
  module will be the name that the user needs to specify when
  invoking `bumblebee-status` (i.e. a module called `modules/contrib/test.py`
  will be loaded using `bumblebee-status -m test`)
- See below for how to actually write the module
- Test (run `bumblebee-status` in the CLI)
- Make sure your changes don't break anything: `./coverage.sh`

## Pull requests
The project **gladly** accepts PRs for bugfixes, new functionality, new
modules, etc.
When you feel comfortable with what you've developed, please just open
a PR, somebody will look at it eventually :) Thanks!

## Hello world
This example will show "hello world" in the status bar:

```
"""Short description"""

import core.module
import core.widget

class Module(core.module.Module):
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.full_text))

    def full_text(self, widgets):
        return "hello world"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
```

## `update` vs. `full_text`
TODO

## TODOs
- default update interval
- scrolling
- 
