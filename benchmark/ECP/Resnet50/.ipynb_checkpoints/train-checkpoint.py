import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, SubsetRandomSampler
import time
import numpy as np

# Set up device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define transformations for the training set
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load the ImageNet training dataset
train_dataset = datasets.ImageFolder(root='./imagenet-mini/train', transform=train_transforms)

# Split the dataset into two halves
dataset_size = len(train_dataset)
indices = list(range(dataset_size))
np.random.shuffle(indices)
split = int(np.floor(0.5 * dataset_size))
first_half_indices = indices[:split]
second_half_indices = indices[split:]

# Function to create a DataLoader for a subset of the dataset
def get_dataloader(subset_indices, batch_size=400, num_workers=32):
    subset_sampler = SubsetRandomSampler(subset_indices)
    return DataLoader(train_dataset, batch_size=batch_size, sampler=subset_sampler, num_workers=num_workers)

# Create DataLoaders for each half of the dataset
train_loader_first_half = get_dataloader(first_half_indices)
train_loader_second_half = get_dataloader(second_half_indices)

# Load the pre-trained ResNet-50 model
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

# Modify the final fully connected layer to match the number of classes in ImageNet (1000 classes)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 1000)

# Move the model to the appropriate device (GPU or CPU)
model = model.to(device)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# Training loop
num_epochs = 1
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    data_transfer_time = 0.0
    computation_time = 0.0
    
    # Start with the first half of the dataset
    t0 = time.time()
    for train_loader in [train_loader_first_half, train_loader_second_half]:
        for i, (inputs, labels) in enumerate(train_loader):
            # Measure data preparation time (loading and transformation)
            inputs, labels = inputs, labels        
            # Measure data transfer time from CPU to GPU
            start_event = torch.cuda.Event(enable_timing=True)
            end_event = torch.cuda.Event(enable_timing=True)
            
            start_event.record()
            inputs, labels = inputs.to(device), labels.to(device)
            end_event.record()
            torch.cuda.synchronize()  # Wait for the events to be recorded
            
            batch_transfer_time = start_event.elapsed_time(end_event)  # Time in milliseconds
            data_transfer_time += batch_transfer_time

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Measure computation time on GPU
            start_event.record()
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward pass and optimization
            loss.backward()
            optimizer.step()
            end_event.record()
            torch.cuda.synchronize()

            batch_computation_time = start_event.elapsed_time(end_event)  # Time in milliseconds
            computation_time += batch_computation_time

            running_loss += loss.item()

    t1 = time.time()
    data_loading_time = (t1 - t0) - (data_transfer_time / 1000) - (computation_time / 1000)

    # Print the results
    print(f'Epoch [{epoch+1}/{num_epochs}]')
    print(f'Batch Loading Time (s): {data_transfer_time/1000:.2f}')
    print(f'Total Computation Time (s): {computation_time/1000:.2f}')
    print(f'Data Loading (Disk->DRAM) Time (s): {data_loading_time:.2f}')

