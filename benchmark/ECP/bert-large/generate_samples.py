import tensorflow as tf
import random

def multiply_tfrecords(input_tfrecord, output_tfrecord_base, multipliers):
    # Read the original TFRecord once into memory
    records = []
    for record in tf.data.TFRecordDataset(input_tfrecord):
        records.append(record.numpy())
    
    original_size = len(records)
    print(f"Original number of records: {original_size}")
    
    for multiplier in multipliers:
        # Calculate the number of records to be output
        num_output_records = int(original_size * multiplier)
        output_tfrecord = f"{output_tfrecord_base}_{num_output_records}_samples.tfrecord"
        
        # Randomly sample records if the multiplier is less than 1
        if multiplier < 1:
            selected_records = random.sample(records, num_output_records)
        else:
            # Repeat the original records if the multiplier is greater than 1
            selected_records = records * int(multiplier)
            selected_records += random.sample(records, num_output_records - len(selected_records))

        # Write to the new TFRecord file
        with tf.io.TFRecordWriter(output_tfrecord) as writer:
            for record in selected_records:
                writer.write(record)
        
        print(f"Generated {output_tfrecord} with {num_output_records} records.")

if __name__ == "__main__":
    input_tfrecord = "6000_samples"  # Path to your input TFRecord file
    output_tfrecord_base = "output"  # Base name for the output TFRecord files
    
    # Multipliers to increase the TFRecords (e.g., 0.1 for 10%, 2 for 2x, etc.)
    multipliers = [0.1]
    
    # Call the function to create multiple output files with multiplied records
    multiply_tfrecords(input_tfrecord, output_tfrecord_base, multipliers)
    
    print("All multiplied TFRecords have been generated.")
