from tqdm import tqdm

import mimetypes
import requests
import json
import os

from sklearn.metrics import classification_report

if __name__ == "__main__":

    if not os.path.exists("check.json"):

        check = {}

        for claim_folder in tqdm(os.listdir('./data/tests')):
            claim_path = os.path.join('./data/tests', claim_folder)
            if os.path.isdir(claim_path):
                files = []
                for file in os.listdir(claim_path):
                    file_path = os.path.join(claim_path, file)
                    if 'answer.json' in file_path:
                        with open(file_path, 'r') as f:
                            expected_answer = json.load(f)
                        check[claim_folder] = {'expected': expected_answer}
                        continue
                    if os.path.isfile(file_path):
                        media_type, _ = mimetypes.guess_type(file_path)
                        files.append(('files', (file, open(file_path, 'rb'), media_type)))
                response = requests.post('http://127.0.0.1:8000/claims', files=files)
                check[claim_folder]['actual'] = response.json()

        with open("./data/check.json", "w") as file:
            json.dump(check, file, indent=4)

    with open("./data/check.json", "r") as file:
        check = json.load(file)

    y_true = []
    y_pred = []
    for claim_id, result in check.items():
        expected = result['expected']['decision']
        actual = result['actual']['decision']
        if 'acceptable_decision' in result['expected'] and expected != actual:
            expected = result['expected']['acceptable_decision']
        y_true.append(expected)
        y_pred.append(actual)

    print(classification_report(y_true, y_pred, target_names=['APPROVE', 'DENY', 'UNCERTAIN']))

    # PRint how many are approve, deny and uncertain in both models compared
    approve_expected = 0
    deny_expected = 0
    uncertain_expected = 0
    approve_actual = 0
    deny_actual = 0
    uncertain_actual = 0
    matches = 0
    total = 0
    for claim_id, result in check.items():
        expected = result['expected']['decision']
        actual = result['actual']['decision']
        if expected == actual:
            matches += 1

        if expected == "APPROVE":
            approve_expected += 1
        elif expected == "DENY":    
            deny_expected += 1
        elif expected == "UNCERTAIN":
            uncertain_expected += 1

        if actual == "APPROVE":
            approve_actual += 1
        elif actual == "DENY":    
            deny_actual += 1
        elif actual == "UNCERTAIN":
            uncertain_actual += 1
        
        total += 1

    print(f"Matches: {matches}/{total} ({matches/total:.2%})")
    print(f"Approve: {approve_actual}/{approve_expected}") 
    print(f"Deny: {deny_actual}/{deny_expected}")
    print(f"Uncertain: {uncertain_actual}/{uncertain_expected} ")
