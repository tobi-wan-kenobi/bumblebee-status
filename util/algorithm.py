import copy


def merge(target, *args):
    """Merges arbitrary data - copied from http://blog.impressiver.com/post/31434674390/deep-merge-multiple-python-dicts

    :param target: the data structure to fill
    :param args: a list of data structures to merge into target

    :return: target, with all data in args merged into it
    :rtype: whatever type was originally passed in
    """
    if len(args) > 1:
        for item in args:
            merge(target, item)
        return target

    item = args[0]
    if not isinstance(item, dict):
        return item
    for key, value in item.items():
        if key in target and isinstance(target[key], dict):
            merge(target[key], value)
        else:
            if not key in target:
                target[key] = copy.deepcopy(value)
    return target


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
