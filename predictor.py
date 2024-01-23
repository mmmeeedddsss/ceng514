import json
import random
import subprocess
from tqdm import tqdm
from functools import lru_cache

from utils import SimilarityCalculator
from data_access import SpiderDataset
from gpt import OpenAIWrapper


class Predictor:
    def __init__(self, output_file_path='predicted_queries.sql'):
        self.dataset = SpiderDataset()
        self.output_file_path = output_file_path
        self.similarity_calc = SimilarityCalculator(self.dataset.training_queries + self.dataset.dev_queries)

    def sample_dataset(self, num_samples=100):
        sampled_queries = random.sample(self.dataset.dev_queries, num_samples)
        self.save_truths_for_eval(sampled_queries)
        return sampled_queries

    @lru_cache
    def find_similar_items(self, user_question):
        return self.similarity_calc.sentence_vector(user_question, 8)

    def user_prompt(self, user_question, db_id):
        similar_items = self.find_similar_items(user_question)

        predicted_query = OpenAIWrapper.generate_sql_for_promt(
            database_name=db_id,
            database_tables=self.dataset.format_tables_short(db_id),
            user_prompt=user_question,
            similar_items=similar_items
        )
        # Remove multiple whitespaces and newlines
        return ' '.join(predicted_query.replace('\n', ' ').split())

    def predict(self, num_samples=0, start_from=0, step_size=100):
        print('Predicting for num_samples:', num_samples, 'start_from:', start_from, 'step_size:', step_size)
        if num_samples == -1:
            sampled_queries = self.dataset.dev_queries
            sampled_queries = sampled_queries[start_from:start_from + step_size]
            self.save_truths_for_eval(sampled_queries)
        else:
            sampled_queries = self.sample_dataset(num_samples=num_samples)

        predicted_queries = []
        for example in tqdm(sampled_queries):
            db_id = example['db_id']
            question = example['question']

            similar_items = self.similarity_calc.sentence_vector(question, 8)
            predicted_query = OpenAIWrapper.generate_sql_for_promt(
                database_name=db_id,
                database_tables=self.dataset.format_tables_short(db_id),
                user_prompt=question,
                similar_items=similar_items
            )

            # Remove multiple whitespaces and newlines
            predicted_query = ' '.join(predicted_query.replace('\n', ' ').split())
            predicted_queries.append(predicted_query)

        self.save_preds_for_eval(predicted_queries, start_from, step_size)

        return predicted_queries

    def save_preds_for_eval(self, predicted_queries, start_from, step_size):
        self.output_file_path = f'predicted_queries_{start_from}_{start_from + step_size}.sql'

        with open(self.output_file_path, 'w') as f:
            for line in predicted_queries:
                f.write(line + '\n')

        with open('predicted_queries.sql', 'a+') as f:
            for line in predicted_queries:
                f.write(line + '\n')

    def save_truths_for_eval(self, sampled_queries, ):
        with open('sampled_truth.json', 'w') as f:
            json.dump(sampled_queries, f, indent=4)

        with open('sampled_truth_sqls.sql', 'w') as f:
            query_strings = [(c['query'], c['db_id']) for c in sampled_queries]
            for q, db in query_strings:
                f.write(f'{q} \t {db}\n')

    def evaluate(self, table='spider/dataset/tables.json',
                 gold='sampled_truth_sqls.sql',
                 db_dir='spider/dataset/database',
                 etype='all'):

        pred = self.output_file_path

        subprocess.run(["python", "spider/evaluator/evaluation.py",
                        "--gold", gold,
                        "--pred", pred,
                        "--db", db_dir,
                        "--table", table,
                        "--etype", etype])
