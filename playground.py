import json

from data_access import SpiderDataset
import random

from predictor import Predictor

random.seed(41)

"""
queries = Predictor().sample_dataset(10)
print(OpenAIWrapper.translate_to_turkish(user_promt_list=[q['question'] for q in queries]))
"""


"""

queries = Predictor().sample_dataset(10)
user_promt_list = [(q['query'], q['question']) for q in queries]
for query, question in user_promt_list[:10]:
    print(f"Question: \n {question.strip()}")
    print()
    print(f"Query: \n {query.strip()}")
exit()
"""

"""
dataset = SpiderDataset()
print(OpenAIWrapper.generate_sql_for_promt(
    database_name='concert_singer',
    database_tables=dataset.format_tables_short('concert_singer'),
    user_prompt='Fransız şarkıcıların ortalama, maksimum ve mimimum yaşları nelerdir?')
)
"""

"""
p = Predictor(use_turkish=True)
p.predict(10)
print('*** evaluating for turkish ***')
p.evaluate()
"""

p = Predictor(use_turkish=False)
p.predict(3)
print('*** evaluating for english ***')
p.evaluate()

"""

python spider/evaluator/evaluation.py \
    --gold sampled_truth_sqls.sql \
    --pred predicted_queries.sql \
    --db spider/dataset/database \
    --table spider/dataset/tables.json \
    --etype all
    
"""
