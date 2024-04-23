import random, json
import json

def loadData(file):
    with open(file, 'r', encoding="utf8") as f:
        data = f.readlines()
    result = []
    for d in data:
        d = d.strip()
        if (len(d) > 0):
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

json_messages = []
for _ in range(250):
    selected_requests = random.sample(train_bad_requests, 5)  # 10개의 요청을 무작위로 선택
    json_message = {
        "messages": [
            {"role": "system", "content": "Examine the following 10 HTTP requests and classify as either normal or anomalous. The answer should be either anormalous or normal"},
            {"role": "user", "content": " ".join(selected_requests)},
            {"role": "assistant", "content": "anomalous"}
        ]
    }
    json_messages.append(json_message)

for _ in range(250):
    selected_requests = random.sample(train_good_requests, 5)  # 10개의 요청을 무작위로 선택
    json_message = {
        "messages": [
            {"role": "system", "content": "Examine the following 10 HTTP requests and classify as either normal or anomalous. The answer should be either anormalous or normal"},
            {"role": "user", "content": " ".join(selected_requests)},
            {"role": "assistant", "content": "normal"}
        ]
    }
    json_messages.append(json_message)

# .jsonl 파일로 저장
jsonl_file_path = 'http-fine-tuning.jsonl'
with open(jsonl_file_path, 'w', encoding="utf8") as f:
    for message in json_messages:
        json_line = json.dumps(message) + "\n"
        f.write(json_line)
