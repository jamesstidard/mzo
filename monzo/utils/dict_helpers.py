from collections.__init__ import OrderedDict

from ordered_set import OrderedSet


def unify_dicts(dicts, *, key_order=None, fill=None):
    if not key_order:
        key_order = OrderedSet(k for d in dicts for k in d.keys())

    filtered_dicts = [{k: v for k, v in d.items() if k in key_order}
                      for d in dicts]

    empty_template = {k: fill for k in key_order}
    filled_dicts = [{**empty_template, **d} for d in filtered_dicts]

    column_order = key_sorter(*key_order)
    sorted_dicts = [OrderedDict(sorted(d.items(), key=column_order))
                    for d in filled_dicts]

    return sorted_dicts


def key_sorter(*key_order):
    """
    Sort dictionary keys by provided order.

    This returns a function that cant be used as a key for a sort function,
    such as `fn` in `sorted(a, key=fn)`.
    """
    def column_index(dict_item):
        key, _ = dict_item
        try:
            return key_order.index(key)
        except ValueError:
            return float('infinity')
    return column_index
