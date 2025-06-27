import tensorflow as tf
import os
import glob

def double_tfrecord_size(input_file):
    # Read the original TFRecord file
    dataset = tf.data.TFRecordDataset(input_file)
    
    # Create a TFRecord writer to overwrite the original file
    writer = tf.io.TFRecordWriter(input_file)
    
    for record in dataset:
        # Write each record twice to double the size
        writer.write(record.numpy())  # Write the original record
        writer.write(record.numpy())  # Write the duplicate of the same record
    
    writer.close()

def iterate_and_double_tfrecords(directory):
    # Find all .tfrecord files under the directory
    tfrecord_files = glob.glob(os.path.join(directory, "*.tfrecord"))
    
    for tfrecord_file in tfrecord_files:
        print(f"Doubling size of {tfrecord_file}")
        double_tfrecord_size(tfrecord_file)

# Example usage: Provide the directory containing TFRecord files
directory = "./tf_records/train/"
iterate_and_double_tfrecords(directory)
