import os
import random

from predictor import Predictor

random.seed(41)


start_from = int(os.environ.get("START_FROM_ROW"))
step_size = int(os.environ.get("STEP_SIZE"))

p = Predictor(output_file_path='predicted_queries.sql')
p.predict(num_samples=-1, start_from=start_from, step_size=step_size)


tables_json_path = os.environ.get("TABLES_JSON_PATH")
gold_sql_path = os.environ.get("GOLD_SQL_PATH")
db_path = os.environ.get("DB_PATH")  # spider/dataset/database

p.evaluate(table=tables_json_path, gold=gold_sql_path, db_dir=db_path)
