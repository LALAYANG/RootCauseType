INPUT=$1
MODEL=$2

echo START $(date +%Y-%m-%d)

mkdir -p results
SAVE_PATH="results/root_cause_eval_$(basename $INPUT .json)_${MODEL}.jsonl"

echo INPUT: $INPUT
echo MODEL: $MODEL
echo SAVE_PATH: $SAVE_PATH

python3 prompt_model.py --input_json $INPUT --model $MODEL --save_path $SAVE_PATH

echo END $(date +%Y-%m-%d)