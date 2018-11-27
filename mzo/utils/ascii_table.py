from terminaltables import AsciiTable

from mzo.utils.dict_helpers import unify_dicts


def ascii_table(dicts=None, columns=None, title=None, fill='-', justify_columns=None):
    if dicts:
        sorted_dicts = unify_dicts(dicts, key_order=columns, fill=fill)
        row_values = [d.values() for d in sorted_dicts]

        table = AsciiTable([[str(c) for c in columns]] + row_values, title=title)

        if justify_columns:
            justifications = {i: justify_columns.get(c, 'left') for i, c in enumerate(columns)}
            table.justify_columns = justifications

        return table.table
    else:
        return AsciiTable([['no results to display']], title=title or 'message').table
