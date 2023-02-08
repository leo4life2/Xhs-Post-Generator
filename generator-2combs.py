# coding=utf8

import csv
import os
import openai
import numpy as np
openai.api_key = os.getenv("OPENAI_API_KEY")
import sys

TRAINING_DATA_FILE = sys.argv[1]
OUTPUT_FILE_NAME = sys.argv[2]
MAX_RESULTS = int(sys.argv[3])
PROMPT_PREFIX = ""
PROMPT_SUFFIX = ""

# Open the file called prompt-prefix.suffix.txt. The firstline is the prompt, the rest is the suffix.
with open("prompt-prefix-suffix.txt", mode='r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    PROMPT_PREFIX = lines[0][len("Prefix: "):]
    PROMPT_SUFFIX = lines[1][len("Suffix: "):]

def get_data():
    all_data = []

    with open(TRAINING_DATA_FILE, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for row in reader:
            all_data.append((row[0], row[1]))

    return all_data

def get_result(title1, content1, title2, content2, fp, pp):

    prompt = PROMPT_PREFIX
    prompt += f"\n标题：{title1}\n内容：{content1}\n\n标题：{title2}\n内容：{content2}\n\n"
    prompt += PROMPT_SUFFIX

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=1212,
        top_p=1,
        frequency_penalty=fp,
        presence_penalty=pp
    )

    return response["choices"][0]["text"]

def get_combs(all_data):
    # get all combinations of 2 of all rows in all_data
    combs = []
    for i in range(len(all_data)):
        for j in range(i+1, len(all_data)):
            combs.append((all_data[i], all_data[j]))

    return combs

def main():
    print("Fetching data...\n")
    all_data = get_data()
    print("Generating combinations...\n")
    combs = get_combs(all_data)

    if MAX_RESULTS != 0 and MAX_RESULTS < len(combs): # limit max # of results
        combs = combs[:MAX_RESULTS]

    results = {}
    fp, pp = 1, 1
    print("Beginning Completions...\n")
    for i, comb in enumerate(combs):
        while True:
            try:
                title1, content1 = comb[0]
                title2, content2 = comb[1]
                print(f"Combination {i+1}/{len(combs)}")
                result = get_result(title1, content1, title2, content2, fp, pp)

                splitted = result.split("内容：")
                content = splitted[1].strip()
                title = splitted[0].split("标题：")[1].strip()

                if (fp, pp) in results:
                    results[(fp, pp)].append((title, content))
                else:
                    results[(fp, pp)] = [(title, content)]
                print("Title: ", title)
                print("Content: ", content)
            except:
                result = get_result(title1, content1, title2, content2, fp, pp)
                print("Retry")
                continue
            break

    with open("output-csvs/" + OUTPUT_FILE_NAME, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        for key in results:
            writer.writerow([f"fp: {key[0]}, pp: {key[1]}"])
            writer.writerows(results[key])

if __name__ == "__main__":
    main()