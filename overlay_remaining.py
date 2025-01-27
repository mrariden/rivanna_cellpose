#!/bin/python3

import argparse
from pathlib import Path
import subprocess
import os


rv_cp_dir = "/scratch/" + os.environ.get('USER') + "/rivanna_cellpose"

def overlay_masks(base_dir, slurm_script):
    """
    """
    base_path = Path(base_dir)

    masks_path = base_path / 'fiber_masks'
    overlays_path = base_path / 'overlay_downscale'
    
    # Remove the /sfs/weka/ where the /scratch dir might be mounted: 
    masks_str = str(masks_path.resolve())
    masks_str = masks_str.split('/sfs/weka')[-1]

    masks = list(masks_path.glob("*.png"))
    overlays = list(overlays_path.glob("*.png"))
    
    mask_names = [n.stem.split('.')[0] for n in masks]
    overlay_names = [n.stem[:-13] for n in overlays]
    
    remaining_masks = [m for m in mask_names if m not in overlay_names]
    
    for m in remaining_masks:
        m_path = masks_path / (m + '.ome_cp_masks.png')
        
        # Remove the /sfs/weka/ where the /scratch dir might be mounted: 
        m_path_str = str(m_path.resolve())
        m_path_str = m_path_str.split('/sfs/weka')[-1]
        
        base_path_str = str(base_path.resolve())
        base_path_str = base_path_str.split('/sfs/weka')[-1]
        
        # Command order: script, mask_path, log_path
        cmd = ['sbatch', slurm_script, m_path_str, base_path_str]
        subprocess.run(cmd)
        

def main():
    parser = argparse.ArgumentParser(description="overlay segmentation masks via SLURM.")
    parser.add_argument("base_dir", type=str, help="Base directory containing mask, overlay, original_image folders.")
    parser.add_argument("-s", "--slurm_script", type=str, 
            default=rv_cp_dir + "/overlay_segmentation.slurm", 
            help="Path to the SLURM script for image overlay."
            f"Default is the slurm script location: '{rv_cp_dir}/overlay_segmentation.slurm'."
            )

    args = parser.parse_args()

    overlay_masks(args.base_dir, args.slurm_script)

if __name__ == "__main__":
    main()

