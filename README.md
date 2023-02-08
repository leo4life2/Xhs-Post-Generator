# Xhs-Post-Generator

## Prerequisites
- OpenAI API Key
- Python 3
- Required Libraries: `openai`, `numpy`

## Usage

1. `export OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. Edit `prompt-prefix-suffix.txt` for your prompt prefix and suffix. In between the prefix and suffix are the two pieces of training data as ICL learning samples.
3. `python3 generator-2combs.py TRAINING_DATA_FILE OUTPUT_FILE_NAME] [MAX_RESULTS]`

`TRAINING_DATA_FILE` is the name of the CSV file containing the training data. The first column should be post titles, and the second column should be post contents. The file should be in the `training-data` directory.

`OUTPUT_FILE_NAME` is the name of the CSV file to output the generated posts to. The file will be in the `outputs-csvs` directory.

OPTIONAL: `MAX_RESULTS` is the maximum number of results we want to generate. The default is 0, which will generate (#samples choose 2) results.

## Examples
```
python3 generator-2combs.py input-csvs/pax-new.csv test-allcombs.csv
```
Takes all the combinations of 2 of all samples in `input-csvs/pax-new.csv`, gives them to GPT3 for in context learning, and generates a result for each combination. The results are written to `outputs-csvs/test-allcombs.csv`.

```
python3 generator-2combs.py input-csvs/pax-new.csv test-5results.csv 5
```
Takes *the first five* combinations of 2 of all samples in `input-csvs/pax-new.csv`, gives them to GPT3 for in context learning, and generates a result for each combination. The results are written to `outputs-csvs/test-5results.csv`.

## Functionality
1. Reads in training data from `TRAINING_DATA_FILE` in CSV format. First column should be post titles, and second column should be post contents.
2. Generates all combinations of two pieces of training data.
3. Calls the OpenAI API with a prompt combining the two pieces of training data and gets the completions.
4. Writes the completions to `OUTPUT_FILE_NAME` in CSV format. First column is the post title, and second column is the post content. The first row is the fp and pp hyperparameters used to generate the post. Outputs are in the `outputs-csvs` directory.