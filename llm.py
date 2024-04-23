import csv
from openai import OpenAI
import random

client = OpenAI(api_key='openai-api-key')

def loadData(file):
    with open(file, 'r', encoding="utf8") as f:
        data = f.readlines()
    result = []
    for d in data:
        d = d.strip()
        if len(d) > 0:
            result.append(d)
    return result

def split_data(data, test_ratio=0.2, seed=None):
    if seed is not None:
        random.seed(seed)
    shuffled_data = random.sample(data, len(data)) 
    test_size = int(len(data) * test_ratio)
    test_set = shuffled_data[:test_size]
    train_set = shuffled_data[test_size:] 
    return train_set, test_set


bad_requests = loadData('anomalousRequestTest.txt')
good_requests = loadData('normalRequestTraining.txt')

train_good_requests, test_good_requests = split_data(good_requests, seed=42)
train_bad_requests, test_bad_requests = split_data(bad_requests, seed=42)

def inference(count, num_requests, csv_file_title):
    with open(csv_file_title, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['data', 'y_pred', 'y_test'])  # CSV 파일의 헤더

        # 첫 번째 for loop - 이상 요청 분류
        for _ in range(count):
            selected_requests = random.sample(test_bad_requests, num_requests)
            request_string = " ".join(selected_requests)
            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0125:personal:stat-ml-project:9GByHFWi",
                messages=[
                    {"role": "system", "content": "Examine the following HTTP requests and classify as either normal or anomalous. The answer should be either anormalous or normal."},
                    {"role": "user", "content": request_string}
                ]
            )
            pred_result = completion.choices[0].message.content
            writer.writerow([request_string, pred_result, 'anomalous'])
            print(f'y_pred: {pred_result}, y_test: anomalous')

        # 두 번째 for loop - 정상 요청 분류
        for _ in range(count):
            selected_requests = random.sample(test_good_requests, num_requests)
            request_string = " ".join(selected_requests)
            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0125:personal:stat-ml-project:9GByHFWi",
                messages=[
                    {"role": "system", "content": "Examine the following HTTP requests and classify as either normal or anomalous. The answer should be either anormalous or normal."},
                    {"role": "user", "content": request_string}
                ]
            )
            pred_result = completion.choices[0].message.content
            writer.writerow([request_string, pred_result, 'normal'])
            print(f'y_pred: {pred_result}, y_test: normal')


inference(100, 1, 'results/classification_results_1requests.csv')

inference(100, 5, 'results/classification_results_5requests.csv')

inference(100, 10, 'results/classification_results_10requests.csv')

