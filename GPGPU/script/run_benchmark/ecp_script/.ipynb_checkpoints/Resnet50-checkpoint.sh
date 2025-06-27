#!/bin/bash

num_gpus=1

# Function to stop the Docker container and kill related processes
cleanup() {
    echo "Stopping Docker container and killing related processes..."
    
    # Stop the container forcefully
    sudo docker stop "$container_id"
    
    # Force remove the container if needed (in case stopping doesn't work)
    sudo docker rm -f "$container_id"
    
    # Kill all remaining Python processes inside the container (if any)
    sudo pkill -f "python3 /workspace/tensorflow2/resnet_ctl_imagenet_main.py"
    
    echo "Cleanup done."
    exit 0
}

# Function to start the Docker training
start_docker_training() {
    # Define the training command with all arguments
    training_command="python3 /workspace/tensorflow2/resnet_ctl_imagenet_main.py \
                    --base_learning_rate=8.5 \
                    --batch_size=128 \
                    --clean \
                    --data_dir=/workspace/tf_records/train \
                    --datasets_num_private_threads=32 \
                    --dtype=fp32 \
                    --device_warmup_steps=1 \
                    --noenable_device_warmup \
                    --enable_eager \
                    --noenable_xla \
                    --epochs_between_evals=1 \
                    --noeval_dataset_cache \
                    --eval_offset_epochs=2 \
                    --eval_prefetch_batchs=192 \
                    --label_smoothing=0.1 \
                    --lars_epsilon=0 \
                    --log_steps=1250000 \
                    --lr_schedule=polynomial \
                    --model_dir=./model \
                    --momentum=0.9 \
                    --num_accumulation_steps=1 \
                    --num_classes=1000 \
                    --num_gpus=$num_gpus \
                    --optimizer=LARS \
                    --noreport_accuracy_metrics \
                    --single_l2_loss_op \
                    --noskip_eval \
                    --steps_per_loop=1252 \
                    --target_accuracy=0.759 \
                    --notf_data_experimental_slack \
                    --tf_gpu_thread_mode=gpu_private \
                    --notrace_warmup \
                    --train_epochs=1 \
                    --notraining_dataset_cache \
                    --training_prefetch_batchs=128 \
                    --nouse_synthetic_data \
                    --warmup_epochs=0 \
                    --weight_decay=0.0002 \
                    --train_steps=500"

    # Start the Docker container in detached mode and get the container ID
    container_id=$(sudo docker run --gpus all --rm -v /home/cc/benchmark/ECP/Resnet50:/workspace -d tensorflow/tensorflow:2.4.0-gpu bash -c "$training_command")

    echo "Docker container started with ID: $container_id"

    # Follow the logs of the running container
    sudo docker logs -f "$container_id" &
    log_pid=$!
    
    # Wait for the container to complete execution
    sudo docker wait "$container_id"
    
    # Wait for log process to finish
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

# Start the Docker training
start_docker_training

