#!/bin/bash

num_images=25

model=models/steve_7b_sft
model_name=cot_qwen2vl

# model=models/UI-TARS-7B-DPO
# model_name=ui-tars
# num_images=5

port=9000

ground_model=models/UI-TARS-7B-DPO

# Function to clean up processes on exit
cleanup() {
    echo "Stopping all processes..."
    pkill -P $$  # Kill all child processes of this script
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM to run cleanup function
trap cleanup SIGINT SIGTERM

# Start processes
for i in {0..6}; do
    CUDA_VISIBLE_DEVICES=$i python -m vllm.entrypoints.openai.api_server \
        --served-model-name $model_name \
        --model $model \
        --limit-mm-per-prompt image=$num_images \
        --chat-template ./chat_template_qwen2vl.jinja \
        -tp=1 \
        --port $((9000 + i)) &
        # --chat-template $model/chat_template.json\ # wrong, use vllm default with low Temperature
done

CUDA_VISIBLE_DEVICES=7 python -m vllm.entrypoints.openai.api_server \
    --served-model-name ui-tars \
    --model $ground_model \
    --chat-template ./chat_template_qwen2vl.jinja \
    -tp=1 \
    --port 8001 &

# Wait to keep the script running
wait