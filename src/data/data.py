from typing import List

import torch
from torch.utils.data import DataLoader
from torchvision.transforms import v2

from .simpsons_dataset import SimpsonsDataset


def get_data_loaders(
    data_path: str,
    size: int,
    batch_size: int,
    val_batch_size: int,
    num_workers: int,
    num_folds: int,
    val_fold: int,
    norm_mean: List[int] = [0.485, 0.456, 0.406],
    norm_std: List[int] = [0.229, 0.224, 0.225],
):
    # Create transforms
    train_tfms = v2.Compose([
        v2.ToImage(),
	v2.RandomHorizontalFlip(),
	v2.RandomRotation(30),
	v2.RandomResizedCrop(size, antialias=True),
	#Data Aug
#    v2.ColorJitter(brightness=0.5, saturation=0.7),
	v2.ToDtype(torch.float32, scale=True),
	v2.Normalize(mean=norm_mean, std=norm_std),
    ])
    val_tfms = v2.Compose([
        v2.ToImage(),
	v2.Resize(size, antialias=True),
	v2.CenterCrop(size),
	v2.ToDtype(torch.float32, scale=True),
	v2.Normalize(mean=norm_mean, std=norm_std),
    ])

    # Create datasets
    ds_train = SimpsonsDataset(data_path, 'train',
                              transform=train_tfms)
    ds_val = SimpsonsDataset(data_path, 'val',
                            transform=val_tfms)

    # Create data loaders
    dl_train = DataLoader(
        ds_train,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )
    dl_val = DataLoader(
        ds_val,
        batch_size=val_batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    return dl_train, dl_val
