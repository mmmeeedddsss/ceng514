import json
from functools import cached_property

from data_model import *


class SpiderDataset:
    @cached_property
    def table_metadata(self):
        with open('spider/dataset/tables.json') as f:
            table_metadata = json.load(f)

        databases = {}
        for raw_db in table_metadata:
            db_id = raw_db['db_id']

            tables = {}

            original_table_names = raw_db['table_names_original']
            table_names = raw_db['table_names_original']

            for table_name in zip(table_names, original_table_names):
                table = Table(name=table_name[0], original_name=table_name[1], columns=[])
                tables[table.name] = table

            column_names = raw_db['column_names_original']
            original_column_names = raw_db['column_names_original']
            column_types = raw_db['column_types']
            foreign_keys = raw_db['foreign_keys']
            primary_keys = raw_db['primary_keys']

            for i, column in enumerate(zip(column_names, original_column_names, column_types)):

                parsed_column = Column(name=column[0][1], original_name=column[1][1], data_type=column[2])
                if i in foreign_keys:
                    parsed_column.foreign_key_of = ForeignKey(table=None, column=None)  # TODO parse
                if i in primary_keys:
                    parsed_column.is_primary_key = True

                if column[0][0] == -1:
                    continue
                table_index = column[0][0]

                tables[table_names[table_index].replace(' ', '_')].columns.append(parsed_column)

            databases[db_id] = Database(name=db_id, tables=tables)

        return databases

    def format_tables_short(self, db_id):
        s = ''
        for table in self.table_metadata[db_id].tables.values():
            s += f'{table.name}'
            s += ' '
            s += '('
            s += ', '.join([f"{c.name} {c.data_type}" for c in table.columns])
            s += ')'
            s += '\n'
        return s

    @cached_property
    def training_queries(self):
        with open('spider/dataset/train_spider.json') as f:
            queries = json.load(f)
        return queries  # has question, db_id, query

    @cached_property
    def dev_queries(self):
        with open('spider/dataset/dev.json') as f:
            queries = json.load(f)
        return queries  # has question, db_id, query