# METU Ceng514
_2023 Fall METU Ceng514 Data Mining project of Egement Berk Galatalı & Mert Tunç_

The repository contains implementations of following two papers with a novel take on similar question selection
- C3: Zero-shot Text-to-SQL with ChatGPT(https://arxiv.org/abs/2307.07306)
- Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation(https://arxiv.org/abs/2308.15363)


## To setup environment

1. Create a folder named spider locally, and download the spider dataset inside. You can find the dataset from https://yale-lily.github.io/spider

The structure should be like `spider/dataset/tables.json`

2. Checkout evaluator next to the dataset folder with name evaluator
```
cd spider
git clone git@github.com:taoyds/spider.git
```
It should look like `spider/evaluator/evaluation.py`

3. In your first run, evaluator will complain about a missing file and will tell what to do. Do it xd


## To run the code

- `demo_webpage.py` provides the demo page of the application. You can see how the app is used and mimic the use for your own implementation. It is run by `streamlit run webpage.py`
- `playground.py` also exemplifies some pipeline usages. The following is enough for running the pipeline for the dev set of Spider dataset.
  ```PYTHON
  from predictor import Predictor
  
  p = Predictor(use_turkish=False)
  p.predict(num_samples=1000)
  p.evaluate()
  ```
This will print the result of evaluator.py provided by the Spider Dataset to stdout.
