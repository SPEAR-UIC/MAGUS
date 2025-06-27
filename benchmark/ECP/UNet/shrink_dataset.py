import os
import shutil
import math

# Directories
dir_imgs = './data/imgs'         # Original images directory
dir_masks = './data/masks'       # Original masks directory
dir_imgs_small = './data/imgs_small'  # Directory to save 20% images
dir_masks_small = './data/masks_small'  # Directory to save 20% masks

# Create directories if they don't exist
os.makedirs(dir_imgs_small, exist_ok=True)
os.makedirs(dir_masks_small, exist_ok=True)

# List all files in the images and masks directories
img_files = sorted(os.listdir(dir_imgs))
mask_files = sorted(os.listdir(dir_masks))

# Ensure both directories contain the same number of files
assert len(img_files) == len(mask_files), "Number of image files and mask files must match."

# Calculate the number of files corresponding to 20%
subset_size = math.ceil(len(img_files) * 0.2)

# Select the first 20% of the files
img_files_subset = img_files[:subset_size]
mask_files_subset = mask_files[:subset_size]

# Copy the first 20% of image and mask files to their respective small directories
for img_file, mask_file in zip(img_files_subset, mask_files_subset):
    # Copy image
    shutil.copy(os.path.join(dir_imgs, img_file), os.path.join(dir_imgs_small, img_file))
    
    # Copy mask
    shutil.copy(os.path.join(dir_masks, mask_file), os.path.join(dir_masks_small, mask_file))

print(f"Copied {subset_size} images and masks to 'imgs_small' and 'masks_small' directories.")
