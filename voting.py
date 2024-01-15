import json

from sqlite_executor import sqlite_executor
import mmh3


def vote_for_most_common_execution(database_name, predicted_queries):
    hash_to_query = {}
    hash_counts = {}
    errors = 0
    for query in predicted_queries:
        try:
            result = sqlite_executor.execute(database_name, query)
        except:
            errors += 1
            continue
        hash_result = mmh3.hash(str(result))
        hash_to_query[hash_result] = query
        if hash_result not in hash_counts:
            hash_counts[hash_result] = 0
        hash_counts[hash_result] += 1

    try:
        most_common_hash = max(hash_counts, key=hash_counts.get)
        print(f'Winner vote count: {hash_counts[most_common_hash]}/{len(predicted_queries)-errors}')
        return hash_to_query[most_common_hash]
    except: # Meaning all queries given is incorrect
        print("All given queries were incorrect!")
        return predicted_queries[0]


def vote_for_common_tables(related_tables_multi):
    voted_tables = {}
    for related_tables in related_tables_multi:
        try:
            parsed_related_tables = json.loads(related_tables)
        except:
            continue
        for table in list(set(parsed_related_tables[:4])):
            if table not in voted_tables:
                voted_tables[table] = 0
            voted_tables[table] += 1

    most_voted_tables = sorted(voted_tables, key=voted_tables.get, reverse=True)[:4]
    return most_voted_tables


def vote_for_common_columns(related_columns_multi):
    """
    {
    "table_1": ["column_1", "column_2", ......],
    "table_2": ["column_1", "column_2", ......],
    "table_3": ["column_1", "column_2", ......],
    ......
    }
    """
    voted_columns_by_table = {}
    for related_columns in related_columns_multi:
        try:
            parsed_related_columns = json.loads(related_columns)
        except:
            continue
        for table, columns in parsed_related_columns.items():
            if table not in voted_columns_by_table:
                voted_columns_by_table[table] = {}
            for column in list(set(columns[:4])):
                if column not in voted_columns_by_table[table]:
                    voted_columns_by_table[table][column] = 0
                voted_columns_by_table[table][column] += 1


    most_voted_columns_by_table = {}
    for table in voted_columns_by_table:
        most_voted_columns_by_table[table] = sorted(voted_columns_by_table[table], key=voted_columns_by_table[table].get, reverse=True)[:4]

    voted_columns = []
    for table, columns in most_voted_columns_by_table.items():
        for column in columns:
            voted_columns.append(column)
    return voted_columns


