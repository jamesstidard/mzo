import json
from enum import Enum

from mzo.utils import csv
from mzo.utils.ascii_table import ascii_table
from mzo.utils.dict_helpers import unify_dicts


class Format(Enum):
    human = "human"
    json = "json"
    csv = "csv"

    def dumps(self, dicts=None, keys=None, title=None, fill=None, justify_columns=None):
        if self is Format.human:
            return ascii_table(
                dicts=dicts,
                columns=keys,
                title=title,
                fill=fill,
                justify_columns=justify_columns,
            )
        elif self is Format.json:
            dicts = unify_dicts(dicts, key_order=keys, fill=fill)
            return json.dumps(dicts, indent=2)
        elif self is Format.csv:
            dicts = unify_dicts(dicts, key_order=keys, fill=fill)
            return csv.dumps(dicts)
        else:
            raise NotImplementedError("Unknown output format", self)
