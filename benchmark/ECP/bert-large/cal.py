import tensorflow as tf

def count_tfrecord_samples(tfrecord_file):
    count = 0
    for record in tf.data.TFRecordDataset(tfrecord_file):
        count += 1
    return count

# Replace this with your actual TFRecord file path
tfrecord_file = "./tf_record/part-00001-of-00500"

sample_count = count_tfrecord_samples(tfrecord_file)
print(f'Total number of samples: {sample_count}')
