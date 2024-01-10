import os
import torch

from torchvision.io import read_image, ImageReadMode
from torchvision.ops.boxes import masks_to_boxes
from torchvision import tv_tensors
from torchvision.transforms.v2 import functional as F
from torch.utils.data import Dataset
import numpy as np
from PIL import Image


class SolarPanelDataset(Dataset):
    def __init__(self, root, transforms):
        # root directory for the dataset
        self.root = root
        # transformations to be applied on the images and masks
        self.transforms = transforms

        # os.path.join is used to combine parts of a path in a platform-independent way
        # os.listdir returns a list of all files in the specified directory
        # sorted() is used to sort the list of files, ensuring that the images and masks align

        # load all image files from the "images" directory inside the root directory
        self.imgs = list(sorted(os.listdir(os.path.join(root, "img"))))
        # load all mask files from the "masks" directory inside the root directory
        self.masks = list(sorted(os.listdir(os.path.join(root, "mask"))))

    def __getitem__(self, idx):
        # load images and masks
        img_path = os.path.join(self.root, "img", self.imgs[idx])
        img = read_image(img_path, mode=ImageReadMode.RGB)

        mask_path = os.path.join(self.root, "mask", self.masks[idx])
        mask = read_image(mask_path, mode=ImageReadMode.RGB)
        # instances are encoded as different colors
        obj_ids = torch.unique(mask)
        # first id is the background, so remove it
        obj_ids = obj_ids[1:]
        num_objs = len(obj_ids)

        # split the color-encoded mask into a set of binary masks
        masks = (mask == obj_ids[:, None, None]).to(dtype=torch.uint8)

        # get bounding box coordinates for each mask
        boxes = masks_to_boxes(masks)

        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)

        image_id = idx
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        # Wrap sample and targets into torchvision tv_tensors:
        img = tv_tensors.Image(img)

        target = {}
        target["boxes"] = tv_tensors.BoundingBoxes(
            boxes, format="XYXY", canvas_size=F.get_size(img)
        )
        target["masks"] = tv_tensors.Mask(masks)
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            if isinstance(img, Image.Image) or isinstance(img, np.ndarray):
                img = self.transforms(img)  # earlier version had (img, target)

        return img, mask, target

    def __len__(self):
        return len(self.imgs)
