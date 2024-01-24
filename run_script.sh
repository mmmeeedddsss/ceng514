#!/bin/bash

export OPENAI_API_KEY=<key>
export TRAIN_SPIDER_JSON_PATH=spider/dataset/train_spider.json
export DEV_JSON_PATH=spider/dataset/dev.json
export DB_PATH=spider/dataset/database
export TABLES_JSON_PATH=spider/dataset/tables.json
export GOLD_SQL_PATH=sampled_truth_sqls.sql  # For merged sqls, use: export GOLD_SQL_PATH=dev_gold.sql


export STEP_SIZE=200
for i in {0..5}
do
    echo "Run $i"

    export START_FROM_ROW=$(( $STEP_SIZE*i ))
    echo "Start from row: $START_FROM_ROW"
    echo "End at row: $(( $START_FROM_ROW + $STEP_SIZE ))"

    python playground.py
done


python spider/test-suite-sql-eval/evaluation.py --gold spider/dataset/dev_gold.sql --pred predicted_queries.sql --db $DB_PATH --table $TABLES_JSON_PATH --etype all


