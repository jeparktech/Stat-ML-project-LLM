import urllib.parse
import io
import os

normal_file_raw = 'source_data/normalTrafficTest.txt'
anomaly_file_raw = 'source_data/anomalousTrafficTest.txt'


normal_file_parse = 'normalRequestTest.txt'
anomaly_file_parse = 'anomalousRequestTest.txt'

def parse_requests(file_in, file_out):
    with open(file_in, 'r') as fin, io.open(file_out, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if line.startswith("GET"):
                url = "GET" + line.split(" ")[1]
                decoded_url = urllib.parse.unquote(url).replace('\n', '').lower()
                fout.write(decoded_url + '\n')
            elif line.startswith("POST") or line.startswith("PUT"):
                parts = line.split()
                method, path = parts[0], parts[1]
                content_length_found = False
                data = ''
                # 다음 줄을 읽으면서 Content-Length를 찾고 그 다음 줄을 데이터로 사용
                for next_line in fin:
                    if next_line.startswith("Content-Length"):
                        content_length_found = True
                        continue
                    if content_length_found:
                        data = next_line.strip()
                        break
                full_url = f"{method}{path}?{data}"
                decoded_url = urllib.parse.unquote(full_url).replace('\n', '').lower()
                fout.write(decoded_url + '\n')
        print(f"Finished parsing requests to {file_out}")

def loadData(file):
    with open(file, 'r', encoding="utf8") as f:
        data = f.readlines()
    result = []
    for d in data:
        d = d.strip()
        if (len(d) > 0):
            result.append(d)
    return result


if not os.path.exists('anomalousRequestTest.txt') or not os.path.exists('normalRequestTest.txt'):
    parse_requests(normal_file_raw, normal_file_parse)
    parse_requests(anomaly_file_raw,anomaly_file_parse)



