# Design
- core: only PSL
- pass if modules are missing
- minimize dependencies, code
- test everything
- think about pylint

# small stuff
- rethink documentation (wiki vs. in-code)
- @parameter? (or was it @attribute?) - remove getter/setters
- use __ for private?

# Features
- new themeing? (and add a "version" for backwards compat?)

## Backwards-compatibility
- aliases
- charts (braille)
- minimize modules
- WAL support / colorscheme support
- tkinter / popups
- scrolling decorator (incl. minwidth, alignment)
- theme.exclude??
- bumblebee-ctrl

## Improvements
- generalize the battery/hbar/vbar concept
- pango output (improve - maybe autodetect? see #531)
- allow handlers to specify whether to update or not (e.g. scroll)
- API documentation
- github pages

## TODO
- theme: `load` vs. `__load` vs. `load_keywords`
- themes: use colors to improve theme readability
- brightness: read from CLI tools
