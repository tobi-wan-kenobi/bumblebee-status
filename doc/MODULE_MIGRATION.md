# Migration of modules

- bumblebee.util.which has been replaced with shutil.which
- bumblebee.engine.Module has been replaced with core.module.Module
- module __init__ has less parameters
- super() works differently
- engine.input.register_callback is now core.input.register
- update() only has a single parameter (self) (no widgets anymore)
- bumblebee.util.format stuff moved into util.format (byte, aslist, asbool, etc.)
- util.format.duration -> shorten -> compact, suffix -> unit
