from collections import OrderedDict

from ordered_set import OrderedSet
from terminaltables import AsciiTable


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


def ascii_table(dicts=None, columns=None, title=None, fill='-'):
    if dicts:
        if not columns:
            columns = OrderedSet(k for d in dicts for k in d.keys())

        filtered_dicts = [{k: v for k, v in d.items() if k in columns}
                          for d in dicts]

        empty_template = {k: fill for k in columns}
        filled_dicts = [{**empty_template, **d} for d in filtered_dicts]

        column_order = key_sorter(*columns)
        sorted_dicts = [OrderedDict(sorted(d.items(), key=column_order))
                        for d in filled_dicts]

        row_values = [d.values() for d in sorted_dicts]

        table = AsciiTable([[str(c) for c in columns]] + row_values, title=title)
        table.justify_columns = {i: 'right' if any(isinstance(r[c], (int, float)) for r in sorted_dicts) else 'left' for i, c in enumerate(columns)}

        return table.table
    else:
        return AsciiTable([['no results to display']], title=title or 'message').table
