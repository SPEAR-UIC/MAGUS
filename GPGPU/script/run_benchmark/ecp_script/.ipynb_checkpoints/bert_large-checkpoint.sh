#!/bin/bash

# 194,052 samples for 1st tf record
num_gpus=1

# Function to start Docker training
cleanup() {
    echo "Stopping Docker container and killing related processes..."
    
    # Stop the container forcefully
    sudo docker stop "$container_id"
    
    # Force remove the container if needed (in case stopping doesn't work)
    sudo docker rm -f "$container_id"
    
    # Kill any remaining Python processes related to the BERT training
    sudo pkill -f "python3 /workspace/run_pretraining.py"
    
    echo "Cleanup done."
    exit 0
}

# Function to start the Docker training
start_docker_training() {
    # Docker image details
    docker_image="tensorflow/tensorflow:2.4.0-gpu"
    
    # Define local and container directories
    local_dir="/home/cc/benchmark/ECP/bert-large"
    container_dir="/workspace"
    
    # Define the training command with logging and pip install
    training_command="cd /workspace/logging && pip install -e . && \
        TF_XLA_FLAGS='--tf_xla_auto_jit=2' python3 /workspace/run_pretraining.py \
        --bert_config_file=/workspace/input_files/bert_config.json \
        --output_dir=/tmp/output/ \
        --input_file=/workspace/6000_samples \
        --do_train=True \
        --iterations_per_loop=1000 \
        --learning_rate=0.0001 \
        --max_eval_steps=1250 \
        --max_predictions_per_seq=76 \
        --max_seq_length=512 \
        --num_gpus=$num_gpus \
        --num_train_steps=750 \
        --num_warmup_steps=0 \
        --optimizer=lamb \
        --save_checkpoints_steps=156200000 \
        --start_warmup_step=0 \
        --train_batch_size=8 \
        --nouse_tpu"

    # Start the Docker container in detached mode and get the container ID
    container_id=$(sudo docker run --gpus all --rm -v "$local_dir:$container_dir" -d "$docker_image" bash -c "$training_command")

    echo "Docker container started with ID: $container_id"

    # Follow the logs of the running container in the background
    sudo docker logs -f "$container_id" &
    log_pid=$!

    # Wait for the container to complete execution
    sudo docker wait "$container_id"
    
    # Wait for the log process to finish
    wait $log_pid

    # Check if the Docker run was successful
    if [ $? -eq 0 ]; then
        echo "Training completed successfully!"
    else
        echo "Error in training."
    fi
}

# Trap Ctrl+C (SIGINT) and call the cleanup function
trap cleanup SIGINT

# Run the training function
start_docker_training

