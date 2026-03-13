import json

from sklearn.metrics import classification_report

if __name__ == "__main__":

    RUN = "run.json"

    with open(f"../data/benchmarks/{RUN}", "r") as file:
        check = json.load(file)

    y_true = []
    y_pred = []
    for claim_id, result in check.items():
        expected = result['expected']['decision']
        actual = result['actual']['result']['decision']
        if 'acceptable_decision' in result['expected'] and expected != actual:
            expected = result['expected']['acceptable_decision']
        y_true.append(expected)
        y_pred.append(actual)

    print(classification_report(y_true, y_pred, target_names=['APPROVE', 'DENY', 'UNCERTAIN']))

    matches = 0
    total = 0
    for claim_id, result in check.items():
        expected = result['expected']['decision']
        actual = result['actual']['result']['decision']
        if 'acceptable_decision' in result['expected'] and expected != actual:
            expected = result['expected']['acceptable_decision']
        if expected == actual:
            matches += 1
        
        total += 1

    print(f"Matches: {matches}/{total} ({matches/total:.2%})")
