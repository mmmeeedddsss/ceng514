import json
import random
import subprocess
from tqdm import tqdm
from functools import lru_cache

from utils import SimilarityCalculator
from data_access import SpiderDataset
from gpt import OpenAIWrapper
from translation_helper import TranslationHelper



class Predictor:
    def __init__(self, use_turkish=False):
        self.dataset = SpiderDataset()
        self.use_turkish = use_turkish
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


    def predict(self, num_samples=100):
        sampled_queries = self.sample_dataset(num_samples=num_samples)

        if self.use_turkish:
            sampled_queries = TranslationHelper.translate_prompts_to_turkish(sampled_queries)

        predicted_queries = []
        for example in tqdm(sampled_queries):
            db_id = example['db_id']
            question = example['question']
            """
            print(f"HERERE {question}")
            if self.use_turkish:
                question = OpenAIWrapper.translate_to_english(question)
                print(question)
            exit
            """

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
