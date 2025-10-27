# Flaky Test Root Cause Category through LLM

## File Structure

```
info_json: information of all Rust flaky tests
scripts: source code
results: model prediction results
```

## Setup

- Set up your github and openai key
```
export OPENAI_API_KEY=[YOUR KEY]
export GITHUB_TOKEN=[YOUR TOKEN]
```
- install requiremtnes  
```
python3 -m venv venv
source venv/bin/activate
pip install requirememts.txt
```

## Prompt model 
```
bash -x scripts/eval.sh input_json [MODEL]
```