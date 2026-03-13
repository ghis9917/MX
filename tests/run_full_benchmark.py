from tqdm import tqdm

import mimetypes
import requests
import json
import os

from sklearn.metrics import classification_report

if __name__ == "__main__":

    if not os.path.exists("../data/benchmarks/run.json"):

        check = {}

        for claim_folder in tqdm(os.listdir('../data/tests')):
            claim_path = os.path.join('../data/tests', claim_folder)
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
                response = requests.post('http://127.0.0.1:8000/claims/', files=files)
                check[claim_folder]['actual'] = response.json()

        with open("../data/benchmarks/run.json", "w") as file:
            json.dump(check, file, indent=4)
    else:
        print("Latest check still saved as run.json, if you want to run a new check, delete or rename the file and run this script again.")