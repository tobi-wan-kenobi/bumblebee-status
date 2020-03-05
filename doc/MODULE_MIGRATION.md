# Migration of modules

- bumblebee.util.which has been replaced with shutil.which
- bumblebee.engine.Module has been replaced with core.module.Module
- module __init__ has less parameters
- super() works differently
- register_callback is now core.input.register
- update() doesn't have a list of widgets anymore

