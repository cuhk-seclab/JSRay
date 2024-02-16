# Automatic Evaluation

For automatic evaluation only.

## Evaluation Steps
- `pip install selenium`
- Comment L21-22 in `test.py`
- `python3 test.py` to check if your browser works.
- Uncomment L21-22 in `test.py`
- `mkdir site`
- Create `site/website1` `site/website2` ... `site/website20` containing the domains (with https prefix) needed for evaluation.
- `./run.sh` to run the evaluation.

## After Evaluation
Use `generate.py` and `generate_self.py` to clean the data and produce log file.