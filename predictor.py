import json
import random
import subprocess
from tqdm import tqdm

from utils import SimilarityCalculator
from data_access import SpiderDataset
from gpt import OpenAIWrapper
from sqlite_executor import sqlite_executor
from translation_helper import TranslationHelper
from voting import vote_for_most_common_execution, vote_for_common_tables, vote_for_common_columns


class Predictor:
    def __init__(self, use_turkish=False):
        self.dataset = SpiderDataset()
        self.use_turkish = use_turkish

    def sample_dataset(self, num_samples=100):
        sampled_queries = random.sample(self.dataset.training_queries, num_samples)
        self.save_truths_for_eval(sampled_queries)
        return sampled_queries

    def predict(self, num_samples=100):
        sampled_queries = self.sample_dataset(num_samples=num_samples)
        similarity_calc = SimilarityCalculator(self.dataset.training_queries)

        if self.use_turkish:
            sampled_queries = TranslationHelper.translate_prompts_to_turkish(sampled_queries)

        predicted_and_selected_queries = []
        predicted_queries = []
        for example in tqdm(sampled_queries):
            # truth_query = example['query']
            db_id = example['db_id']
            question = example['question']
            """
            print(f"HERERE {question}")
            if self.use_turkish:
                question = OpenAIWrapper.tdata_access.pyranslate_to_english(question)
                print(question)
            exit
            """

            all_table_info = self.dataset.format_tables_short(db_id)

            related_tables_multi = OpenAIWrapper.filter_related_tables(db_id, all_table_info, question)
            related_tables = vote_for_common_tables(related_tables_multi)

            all_foreign_keys_of_related_tables = \
                self.dataset.format_foreign_keys_short(db_id, filter_by_tables=related_tables)

            related_columns_multi = \
                OpenAIWrapper.filter_related_columns(db_id,
                                                     self.dataset.format_tables_short(db_id,
                                                                                      filter_by_tables=related_tables),
                                                     all_foreign_keys_of_related_tables, question)

            related_columns = vote_for_common_columns(related_columns_multi)

            database_tables_to_feed = \
                self.dataset.format_tables_short(db_id, filter_by_tables=related_tables,
                                                 filter_by_columns=related_columns)
            foreign_keys_to_feed = \
                self.dataset.format_foreign_keys_short(db_id, filter_by_tables=related_tables,
                                                       filter_by_columns=related_columns)

            similar_items = similarity_calc.sentence_vector(question, 8)

            predicted_queries = OpenAIWrapper.generate_sql_for_prompt_c3_with_examples(
                database_name=db_id,
                database_tables=database_tables_to_feed,
                foreign_keys=foreign_keys_to_feed,
                user_prompt=question,
                similar_items=similar_items,
                N=15
            )

            voted_query = vote_for_most_common_execution(db_id, predicted_queries)
            predicted_and_selected_queries.append(voted_query)

        self.save_preds_for_eval(predicted_and_selected_queries)

        return predicted_and_selected_queries

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
