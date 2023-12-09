import json
import random
import subprocess

from data_access import SpiderDataset
from gpt import OpenAIWrapper
from translation_helper import TranslationHelper


class Predictor:
    def __init__(self, use_turkish=False):
        self.dataset = SpiderDataset()
        self.use_turkish = use_turkish

    def sample_dataset(self, num_samples=10):
        sampled_queries = random.sample(self.dataset.training_queries, num_samples)
        self.save_truths_for_eval(sampled_queries)
        return sampled_queries

    def predict(self, num_samples=10):
        sampled_queries = self.sample_dataset(num_samples=num_samples)
        self.save_truths_for_eval(sampled_queries)

        if self.use_turkish:
            sampled_queries = TranslationHelper.translate_prompts_to_turkish(sampled_queries)

        predicted_queries = []
        for example in sampled_queries:
            truth_query = example['query']
            db_id = example['db_id']
            question = example['question']

            predicted_query = OpenAIWrapper.generate_sql_for_promt(
                database_name=db_id,
                database_tables=self.dataset.format_tables_short(db_id),
                user_prompt=question
            )

            # Remove multiple whitespaces and newlines
            predicted_query = 'SELECT ' + ' '.join(predicted_query.replace('\n', ' ').split())
            predicted_queries.append(predicted_query)

        self.save_preds_for_eval(predicted_queries)


        return predicted_queries

    def save_preds_for_eval(self, predicted_queries):
        with open('predicted_queries.sql', 'w') as f:
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
                 pred='predicted_queries.sql',
                 db_dir='spider/dataset/database',
                 etype='all'):


        subprocess.run(["python", "spider/evaluator/evaluation.py",
                        "--gold", gold,
                        "--pred", pred,
                        "--db", db_dir,
                        "--table", table,
                        "--etype", etype])
