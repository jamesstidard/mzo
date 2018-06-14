from terminaltables import AsciiTable

from mzo.utils.dict_helpers import unify_dicts


def ascii_table(dicts=None, columns=None, title=None, fill='-'):
    if dicts:
        sorted_dicts = unify_dicts(dicts, key_order=columns, fill=fill)
        row_values = [d.values() for d in sorted_dicts]

        table = AsciiTable([[str(c) for c in columns]] + row_values, title=title)
        table.justify_columns = {i: 'right' if any(isinstance(r[c], (int, float)) for r in sorted_dicts) else 'left' for i, c in enumerate(columns)}

        return table.table
    else:
        return AsciiTable([['no results to display']], title=title or 'message').table
