from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import urllib.parse
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import io
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
import os

normal_file_raw = 'source_data/normalTrafficTest.txt'
anomaly_file_raw = 'source_data/anomalousTrafficTest.txt'


normal_file_parse = 'normalRequestTest.txt'
anomaly_file_parse = 'anomalousRequestTest.txt'

def parse_file(file_in, file_out):
    fin = open(file_in)
    fout = io.open(file_out, "w", encoding="utf-8")
    lines = fin.readlines()
    res = []
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("GET"):
            res.append("GET" + line.split(" ")[1])
        elif line.startswith("POST") or line.startswith("PUT"):
            url = line.split(' ')[0] + line.split(' ')[1]
            j = 1
            while True:
                if lines[i + j].startswith("Content-Length"):
                    break
                j += 1
            j += 1
            data = lines[i + j + 1].strip()
            url += '?' + data
            res.append(url)
    for line in res:
        line = urllib.parse.unquote(line).replace('\n','').lower()
        fout.writelines(line + '\n')
    print ("finished parse ",len(res)," requests")
    fout.close()
    fin.close()

def loadData(file):
    with open(file, 'r', encoding="utf8") as f:
        data = f.readlines()
    result = []
    for d in data:
        d = d.strip()
        if (len(d) > 0):
            result.append(d)
    return result

def print_result(X_train, X_test, y_train, y_test, clf, clf_name):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    matrix = confusion_matrix(y_test, y_pred)
    TP, FP = matrix[0]
    FN, TN = matrix[1]
    PPV = (TP * 1.0) / (TP + FP)
    TPR = (TP * 1.0) / (TP + FN)
    TNR = (FP * 1.0) / (TN + FP)
    ACC = (TP + TN) * 1.0 /  (TP + TN + FP + FN)
    F1 = 2.0 * PPV * TPR / (PPV + TPR)
    print ("%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f"%(clf_name,PPV,TPR,TNR,ACC,F1))


if not os.path.exists('anomalousRequestTest.txt') or not os.path.exists('normalRequestTest.txt'):
    parse_file(normal_file_raw,normal_file_parse)
    parse_file(anomaly_file_raw,anomaly_file_parse)



