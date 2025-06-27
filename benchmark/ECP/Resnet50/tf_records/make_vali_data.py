import os
import random
import tensorflow as tf

# Paths to your train and validation directories
train_dir = './train/'
validation_dir = './validation/'

# Get a list of all tfrecord files in train and validation directories
train_files = [os.path.join(train_dir, f) for f in os.listdir(train_dir) if f.startswith('train')]
validation_files = [os.path.join(validation_dir, f) for f in os.listdir(validation_dir) if f.startswith('validation')]

def combine_tfrecords(source_file, dest_file, output_file):
    # Open source and destination tfrecord files for reading
    source_dataset = tf.data.TFRecordDataset(source_file)
    dest_dataset = tf.data.TFRecordDataset(dest_file)

    # Create a new tfrecord file to write combined data
    with tf.io.TFRecordWriter(output_file) as writer:
        for record in dest_dataset:
            writer.write(record.numpy())
        for record in source_dataset:
            writer.write(record.numpy())

# Loop through each validation file and randomly select a train file to combine its data
for validation_file in validation_files:
    random_train_file = random.choice(train_files)
    
    # Create a temporary output file to hold combined data
    temp_output_file = validation_file + "_temp"
    
    # print(f'Combining data from {random_train_file} and {validation_file} into {temp_output_file}')
    combine_tfrecords(random_train_file, validation_file, temp_output_file)
    
    # Replace the original validation file with the combined data
    os.replace(temp_output_file, validation_file)
    # print(f'Replaced original {validation_file} with combined data.')
