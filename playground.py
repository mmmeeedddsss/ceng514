from data_access import SpiderDataset
from gpt import OpenAIWrapper

dataset = SpiderDataset()

print(OpenAIWrapper.generate_sql_for_promt(
    database_name='concert_singer',
    database_tables=dataset.format_tables_short('concert_singer'),
    user_prompt='Fransız şarkıcıların ortalama, maksimum ve mimimum yaşları nelerdir?') #'What is the average, minimum, and maximum age for all French singers?')
)
