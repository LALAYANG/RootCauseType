# Flaky Test Root Cause Category through LLM

## File Structure

```
info_json: JSON files containing issue descriptions and patches 
scripts: Source code
results: Model prediction outputs and evaluation results
```

## Setup

- Set up github and openai keys
```
export OPENAI_API_KEY=[YOUR KEY]
export GITHUB_TOKEN=[YOUR TOKEN]
```
- Install requiremtnes  
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Prompt model 

- Run the following command, output is saved to the `results/` directory:
```
bash -x scripts/eval.sh info_json [MODEL]
```