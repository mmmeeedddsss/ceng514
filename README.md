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
git clone git@github.com:taoyds/test-suite-sql-eval.git
```
It should look like `spider/test-suite-sql-eval/evaluation.py`

3. In your first run, evaluator will complain about a missing file and will tell what to do. Do it xd


## To run the code

Run
```BASH
pip install -r requirements.txt

# Edit the OPENAI_API_KEY param inside the following sh file before running
sh run_script.sh
```

---

`playground.py` also exemplifies some pipeline usages. The following is enough for running the pipeline for the dev set of Spider dataset.
  ```PYTHON
  from predictor import Predictor
  
  p = Predictor(use_turkish=False)
  p.predict(num_samples=1000)
  p.evaluate()
  ```
This will print the result of evaluator.py provided by the Spider Dataset to stdout.

## Current results on dev set

See `results_for_dev` file for whole of the dump.

```
                     easy                 medium               hard                 extra                all                 
count                248                  446                  174                  166                  1034                
=====================   EXECUTION ACCURACY     =====================
execution            0.960                0.946                0.897                0.813                0.920               

====================== EXACT MATCHING ACCURACY =====================
exact match          0.952                0.863                0.874                0.699                0.860               

---------------------PARTIAL MATCHING ACCURACY----------------------
select               0.976                0.972                0.988                0.962                0.974               
select(no AGG)       0.980                0.972                0.988                0.962                0.975               
where                0.981                0.956                0.880                0.824                0.921               
where(no OP)         1.000                0.956                0.930                0.901                0.950               
group(no Having)     0.950                0.891                0.974                0.880                0.905               
group                0.900                0.798                0.974                0.867                0.853               
order                0.864                0.986                0.962                0.872                0.929               
and/or               1.000                0.998                1.000                1.000                0.999               
IUEN                 0.000                0.000                0.944                0.885                0.905               
keywords             0.980                0.981                0.959                0.962                0.973               
---------------------- PARTIAL MATCHING RECALL ----------------------
select               0.976                0.942                0.977                0.916                0.952               
select(no AGG)       0.980                0.942                0.977                0.916                0.953               
where                0.981                0.956                0.936                0.798                0.927               
where(no OP)         1.000                0.956                0.989                0.872                0.956               
group(no Having)     0.950                0.797                0.949                0.835                0.841               
group                0.900                0.714                0.949                0.823                0.793               
order                0.864                0.960                0.909                0.861                0.905               
and/or               1.000                0.998                1.000                0.994                0.998               
IUEN                 0.000                0.000                0.810                0.676                0.750               
keywords             0.980                0.942                0.943                0.916                0.944               
---------------------- PARTIAL MATCHING F1 --------------------------
select               0.976                0.957                0.983                0.938                0.963               
select(no AGG)       0.980                0.957                0.983                0.938                0.964               
where                0.981                0.956                0.907                0.811                0.924               
where(no OP)         1.000                0.956                0.959                0.886                0.953               
group(no Having)     0.950                0.841                0.961                0.857                0.872               
group                0.900                0.754                0.961                0.844                0.822               
order                0.864                0.973                0.935                0.866                0.917               
and/or               1.000                0.998                1.000                0.997                0.999               
IUEN                 1.000                1.000                0.872                0.767                0.820               
keywords             0.980                0.961                0.951                0.938                0.958       
```