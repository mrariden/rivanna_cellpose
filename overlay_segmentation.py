#!/bin/python3

import argparse
from pathlib import Path
import subprocess
import os
import sys

import numpy as np
from PIL import Image
from tqdm.contrib import tzip

Image.MAX_IMAGE_PIXELS = None


def img_to_np(img_file_path):
    img = Image.open(img_file_path)
    img_np = []
    for i in range(3):
        img.seek(i)
        img_np.append(np.array(img))
    img_np = np.array(img_np).astype(float)
    img_np = img_np.transpose((1, 2, 0))
    img_np /= np.max(img_np)
    
    return img_np


def randomize_mask_colors(mask_arr):
    colors = np.random.random((3, np.max(mask_arr)+1))
    colors[:, 0] = [0, 0, 0]
    random_masks = colors.T[mask_arr]
    return random_masks


def overlay_single_mask(mask_path, mask_opacity=0.5, output_path=None):
    
    if output_path is not None: 
        raise NotImplementedError()
    
    mask_path = Path(mask_path)
    
    original_imgs_path = Path(mask_path.parent.parent) / 'original_images' / (mask_path.stem.split('.')[0] + '.ome.tiff')
    
    output_path = Path(mask_path.parent.parent) / 'overlays'
    output_path.mkdir(exist_ok=True)  
    
    output_path_downscale = Path(mask_path.parent.parent) / 'overlay_downscale'
    output_path_downscale.mkdir(exist_ok=True)  
    
    overlay_filename = mask_path.stem.split('.')[0] + '-mask_overlay.png'
    overlay_path = output_path / overlay_filename
    overlay_path_downscale = output_path_downscale / overlay_filename

    i_data = img_to_np(original_imgs_path)
    
    m_data = np.array(Image.open(mask_path))
    m_colored = randomize_mask_colors(m_data)

    # Combine the original image and the mask
    combined_np = np.zeros_like(i_data, dtype=float)
    for c in range(3):  # Combine RGB channels
        combined_np[..., c] = mask_opacity * m_colored[..., c] + (1 - mask_opacity) * i_data[..., c]


    combined_image = Image.fromarray((combined_np * 255.).astype('uint8'))
    
    # print(f"saving to {str(overlay_path)}")
    # combined_image.save(overlay_path)
    
    print(f"saving downscaled overlay to {str(overlay_path_downscale)}")
    size = (combined_image.width // 4, combined_image.height // 4)
    combined_np_resized = combined_image.resize(size)
    combined_np_resized.save(overlay_path_downscale)

def main():
    overlay_single_mask(sys.argv[1])

if __name__ == "__main__":
    main()

