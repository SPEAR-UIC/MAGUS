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