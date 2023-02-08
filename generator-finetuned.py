# coding=utf8

import csv
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_data():
    all_data = []

    with open("pax-cleaned.csv", mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for row in reader:
            all_data.append((row[0], row[1]))

    return all_data

def get_result():
    response = openai.Completion.create(
        model="davinci:ft-personal-2023-01-23-17-57-45",
        prompt="",
        temperature=0.6,
        max_tokens=1212,
        top_p=1,
        frequency_penalty=0.9,
        presence_penalty=0.9
    )

    return response["choices"][0]["text"]

def get_combs(all_data):
    # get all combinations of 2 of all rows in all_data
    combs = []
    for i in range(len(all_data)):
        for j in range(i+1, len(all_data)):
            combs.append((all_data[i], all_data[j]))

    return combs

print(get_result())

# def main():
#     all_data = get_data()
#     combs = get_combs(all_data)
#     results = []

#     for i, comb in enumerate(combs):
#         title1, content1 = comb[0]
#         title2, content2 = comb[1]
#         result = get_result(title1, content1, title2, content2)
#         print(f"Combination {i+1}/{len(combs)}")
#         while True:
#             try:
#                 splitted = result.split("内容：")
#                 content = splitted[1].strip()
#                 title = splitted[0].strip("标题：").strip()

#                 results.append((title, content))
#             except:
#                 result = get_result(title1, content1, title2, content2)
#                 print("Retry")
#                 continue
#             break

#     with open("pax-combs.csv", mode='w', encoding='utf-8-sig', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(results)

# if __name__ == "__main__":
#     main()