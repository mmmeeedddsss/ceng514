from data_access import SpiderDataset
from gpt import OpenAIWrapper

dataset = SpiderDataset()

print(OpenAIWrapper.generate_sql_for_promt(
    database_name='concert_singer',
    database_tables=dataset.format_tables_short('concert_singer'),
    user_prompt='How many singers do we have?')
)
