INPUTS=("info_json" "mp2_fixed_info_json")
MODELS=("gpt-4-turbo" "gpt-5")

echo START $(date +%Y-%m-%d)

DIR_WITH="results_def/results_with_patch"
DIR_NO="results_def/results_no_patch"

mkdir -p "$DIR_WITH" "$DIR_NO"

for INPUT in "${INPUTS[@]}"; do
  for MODEL in "${MODELS[@]}"; do
    BASE_NAME=$(basename "$INPUT" .json)
    SAVE_PATH_WITH="${DIR_WITH}/root_cause_eval_${BASE_NAME}_${MODEL}.jsonl"
    SAVE_PATH_NO="${DIR_NO}/root_cause_eval_${BASE_NAME}_${MODEL}.jsonl"

    echo "---------------------------------------------"
    echo "INPUT: $INPUT"
    echo "MODEL: $MODEL"
    echo "WITH PATCH: $SAVE_PATH_WITH"
    echo "NO PATCH: $SAVE_PATH_NO"
    echo "---------------------------------------------"

    python3 scripts/prompt_model.py \
      --input_json "$INPUT" \
      --model "$MODEL" \
      --save_path "$SAVE_PATH_WITH"

    # Run without patch
    python3 scripts/prompt_model.py \
      --input_json "$INPUT" \
      --model "$MODEL" \
      --save_path "$SAVE_PATH_NO" \
      --no_patch
  done
done

echo END $(date +%Y-%m-%d)
