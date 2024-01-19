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

user_question = "List the names of the books in ascending order"
"""
book_2
List the names of the books in ascending order 

cinema
Select most rated 10 films in ascending order

flight_2
Which country does Airline \"JetBlue Airways\" belong to?
SELECT Country FROM AIRLINES WHERE Airline  =  \"JetBlue Airways\"

flight_2
How many flights depart from City 'Aberdeen' and have destination City 'Ashley'?
SELECT count(*) FROM FLIGHTS AS T1 JOIN AIRPORTS AS T2 ON T1.DestAirport  =  T2.AirportCode JOIN AIRPORTS AS T3 ON T1.SourceAirport  =  T3.AirportCode WHERE T2.City  =  \"Ashley\" AND T3.City  =  \"Aberdeenj"


"""
print(p.user_prompt(user_question, "book_2"))

"""

python spider/evaluator/evaluation.py \
    --gold sampled_truth_sqls.sql \
    --pred predicted_queries.sql \
    --db spider/dataset/database \
    --table spider/dataset/tables.json \
    --etype all
    
"""
