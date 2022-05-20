import csv
import io

from ordered_set import OrderedSet


def dumps(dicts, header=True):
    output = io.StringIO()
    headers = OrderedSet(k for d in dicts for k in d.keys())

    writer = csv.DictWriter(output, fieldnames=headers)
    if header:
        writer.writeheader()
    writer.writerows(dicts)

    return output.getvalue()
