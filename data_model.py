from typing import List, Dict


class ForeignKey:
    def __init__(self, table: "Table", column: "Column"):
        self.table = table
        self.column = column


class Column:
    def __init__(self, name: str, original_name: str, data_type: str, foreign_key_of: ForeignKey = None,
                 is_primary_key=False):
        self.name = name.replace(' ', '_')
        self.original_name = original_name
        self.data_type = data_type
        self.is_primary_key = is_primary_key
        self.foreign_keys = []
        if foreign_key_of:
            self.foreign_keys.append(foreign_key_of)
        self.table: Table = None


class Table:
    def __init__(self, name: str, original_name: str, columns: List[Column]):
        self.name = name.replace(' ', '_')
        self.original_name = original_name
        self.columns = columns


class Database:
    def __init__(self, name: str, tables: Dict[str, Table]):
        self.name = name.replace(' ', '_')
        self.tables = tables
