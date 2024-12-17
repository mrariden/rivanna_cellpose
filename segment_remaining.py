#!/bin/python3

import argparse
from pathlib import Path
import subprocess
import os


rv_cp_dir = "/scratch/" + os.environ.get('USER') + "/rivanna_cellpose"

def segment_images(base_dir, slurm_script):
    """
    Script to segment a folder of images by finding the remaining masks not in the mask dir.
    It then submits a job to SLURM to process each image.

    Args:
    base_dir (str): The base directory where the images and masks are stored.
    slurm_script (str): Path to the SLURM script used for submitting the job.
    mask_output_dir (str): Directory where the output masks should be saved.
    """
    base_path = Path(base_dir)

    original_imgs_path = base_path / 'original_images'
    masks_path = base_path / 'fiber_masks'

    original_imgs = list(original_imgs_path.glob("*.tiff"))
    masks = list(masks_path.glob("*.png"))

    # Iterate through original images, remove existing masks from remaining
    remaining_imgs = original_imgs.copy()

    for o_img in original_imgs:
        o_name = o_img.stem.split('.')[0]

        for mask in masks:
            if o_name in mask.stem:
                remaining_imgs.remove(o_img)
                break

    for img in remaining_imgs:
        # Command order: script, full image path, mask out dir
        cmd = ['sbatch', slurm_script, str(img.resolve()), str(masks_path.resolve())]
        subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Segment images using cellpose via SLURM.")
    parser.add_argument("base_dir", type=str, help="Base directory containing image folders.")
    parser.add_argument("-s", "--slurm_script", type=str, 
            default=rv_cp_dir + "/fiber_seg_CLI_OME-model.slurm", 
            help="Path to the SLURM script for image segmentation."
            f"Default is the slurm script location: '{rv_cp_dir}/fiber_seg_CLI_OME-model.slurm'."
            )

    args = parser.parse_args()

    segment_images(args.base_dir, args.slurm_script)

if __name__ == "__main__":
    main()

