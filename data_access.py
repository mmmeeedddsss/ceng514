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
                table = Table(name=table_name[1], original_name=table_name[1], columns=[])
                tables[table.name] = table

            column_names = raw_db['column_names_original']
            original_column_names = raw_db['column_names_original']
            column_types = raw_db['column_types']
            foreign_keys = raw_db['foreign_keys']
            primary_keys = raw_db['primary_keys']

            columns_by_index = []

            for i, column in enumerate(zip(column_names, original_column_names, column_types)):
                parsed_column = Column(name=column[1][1], original_name=column[1][1], data_type=column[2])
                columns_by_index.append(parsed_column)
                if i in primary_keys:
                    parsed_column.is_primary_key = True

                if column[0][0] == -1:
                    continue
                table_index = column[1][0]

                tables[original_table_names[table_index].replace(' ', '_')].columns.append(parsed_column)
                parsed_column.table = tables[original_table_names[table_index].replace(' ', '_')]

            for i, column in enumerate(zip(column_names, original_column_names, column_types)):
                for fk_indexes in foreign_keys:
                    for fk_index in fk_indexes:
                        if fk_index == i:
                            for k2 in fk_indexes:
                                if k2 == i:
                                    continue
                                current_column = columns_by_index[i]
                                current_column.foreign_key_of = ForeignKey(table=columns_by_index[k2].table, column=columns_by_index[k2])

            databases[db_id] = Database(name=db_id, tables=tables)

        return databases

    def format_tables_short(self, db_id, filter_by_tables=None, filter_by_columns=None):
        s = ''
        for table in self.table_metadata[db_id].tables.values():
            if filter_by_tables and table.name not in filter_by_tables:
                continue

            s += f'{table.name}'
            s += ' '
            s += '('
            s += ', '.join([f"{c.name}" for c in table.columns if
                            filter_by_columns is None or c.name in filter_by_columns])
            s += ')'
            s += '\n'
        return s

    def format_foreign_keys_short(self, db_id, filter_by_tables=None, filter_by_columns=None):
        s = ''
        for table in self.table_metadata[db_id].tables.values():
            if filter_by_tables and table.name not in filter_by_tables:
                continue

            for column in table.columns:
                if filter_by_columns is not None and column.name not in filter_by_columns:
                    continue

                if column.foreign_key_of:
                    lhs = f"{column.table.name}.{column.name}"
                    rhs = f"{column.foreign_key_of.table.name}.{column.foreign_key_of.column.name}"

                    if filter_by_tables is not None and column.foreign_key_of.table.name not in filter_by_tables:
                        continue

                    if filter_by_columns is not None and column.foreign_key_of.column.name not in filter_by_columns:
                        continue


                    if rhs > lhs:
                        s += f'{lhs} = {rhs}'
                        s += '\n'
        return s

    @cached_property
    def training_queries(self):
        with open('spider/dataset/train_spider.json') as f:
            queries = json.load(f)
        return queries  # has question, db_id, query
