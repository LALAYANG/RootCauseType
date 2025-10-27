import argparse
import os
import json
import openai 
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")

ROOT_CAUSE_OPTIONS = [
    "Logic", "Randomness", "Network", "Async Wait", "Concurrency",
    "Time", "I/O", "Unordered data", "Environment"
]

def load_json_files(folder):
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), "r") as f:
                yield json.load(f)

def build_prompt(issue_description, patch):
    return f"""You are an expert in Rust flaky tests. Given the issue description and code patch below, classify the root cause of flaky tests into one of the following categories:

{', '.join(ROOT_CAUSE_OPTIONS)}

Respond only with the exact category name.

### Issue Description:
{issue_description}

### Code Patch:
{patch}
"""

def classify_root_cause(prompt, model):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature= 1 if model == "gpt-5" else 0,
        )
        prediction = response.choices[0].message["content"].strip()
        return prediction
    except Exception as e:
        print("OpenAI API error:", e)
        return None

def evaluate(folder, model, save_path):
    correct = 0
    total = 0

    with open(save_path, "w") as f_out:
        for data in tqdm(load_json_files(folder)):
            gt = data.get("root_cause_category", "")
            if not gt:
                continue
            
            gt = str(gt).strip()
            if gt not in ROOT_CAUSE_OPTIONS:
                continue

            issue = data.get("issue_description", "")
            patch = "\n\n".join(file.get("patch", "") for file in data.get("files_changed", []) if "patch" in file)

            if not issue or not patch:
                continue

            prompt = build_prompt(issue, patch)
            predicted = classify_root_cause(prompt, model)

            if not predicted:
                continue

            match = predicted.lower() == gt.lower()
            result = {
                "id": data["id"],
                "ground_truth": gt,
                "predicted": predicted,
                "match": match,
                "prompt": prompt
            }
            f_out.write(json.dumps(result, ensure_ascii=False) + "\n")

            total += 1
            correct += int(match)

    print(f"\nEvaluated {total} examples")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy: {correct / total:.2%}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate root cause classification using LLM.")
    parser.add_argument("--input_json", type=str, required=True, help="Directory containing input JSON files")
    parser.add_argument("--model", type=str, default="gpt-4")
    parser.add_argument("--save_path", type=str, default="root_cause_eval_full.jsonl")

    args = parser.parse_args()
    evaluate(args.input_json, args.model, save_path=args.save_path)
