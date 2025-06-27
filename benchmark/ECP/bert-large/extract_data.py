import tensorflow as tf

def extract_samples(input_file, output_file, num_samples=6000):
    # Open the original TFRecord file
    dataset = tf.data.TFRecordDataset(input_file)

    # Create a writer for the output file
    writer = tf.io.TFRecordWriter(output_file)

    count = 0
    for record in dataset:
        if count < num_samples:
            writer.write(record.numpy())  # Write to the output file
        else:
            break  # Stop after writing the desired number of samples
        count += 1

    # Close the writer
    writer.close()

    print(f"Finished writing {count} samples to {output_file}.")


# Path to your original TFRecord file
input_tfrecord = "./tf_record/part-00001-of-00500"

# Path for the output TFRecord file
output_tfrecord = "./20000_samples"

# Call the function to extract 6000 samples
extract_samples(input_tfrecord, output_tfrecord, num_samples=20000)
