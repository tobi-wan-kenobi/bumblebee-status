# Design
- core: only PSL
- pass if modules are missing
- minimize dependencies, code
- test everything
- think about pylint

# small stuff
- rethink documentation (wiki vs. in-code)
- @parameter? (or was it @attribute?)
- use __ for private?

# Features

## Backwards-compatibility
- aliases
- icons (prefix/postfix)
- charts (braille)
- minimize modules
- hide modules if not in warning/error state (-a)
- WAL support / colorscheme support
- tkinter / popups
- scrolling decorator (incl. minwidth, alignment)
- states

## Improvements
- pango output (improve - maybe autodetect? see #531)
- only update specific, affected modules when clicking
- allow handlers to specify whether to update or not (e.g. scroll)
