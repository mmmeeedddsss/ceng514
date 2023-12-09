import json

from data_access import SpiderDataset
from gpt import OpenAIWrapper
import random

from predictor import Predictor

random.seed(41)

"""
dataset = SpiderDataset()
print(OpenAIWrapper.generate_sql_for_promt(
    database_name='concert_singer',
    database_tables=dataset.format_tables_short('concert_singer'),
    user_prompt='Fransız şarkıcıların ortalama, maksimum ve mimimum yaşları nelerdir?')
)
"""


p = Predictor()
p.predict(10)
p.evaluate()


"""

python spider/evaluator/evaluation.py \
    --gold sampled_truth_sqls.sql \
    --pred predicted_queries.sql \
    --db spider/dataset/database \
    --table spider/dataset/tables.json \
    --etype all
    
"""