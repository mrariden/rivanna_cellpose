# How to setup & use Cellpose on Rivanna
    Michael Rariden 
    Christ lab, UVA
    12/13/2024


### Overview and usage
This repository contains tools and instructions on how to use cellpose to segment myofibers in muscle tissue cross sections using cellpose on UVA's Rivanna HPC. Rivanna uses SLURM to manage computing resource requests and job submissions. These instructions are written so that each image is submitted as a seperate SLURM job. I describe two ways to set cellpose up; using preinstalled cellpose via software modules (easier), and local installation (harder, but better for customization). 

I highly reccomend using the Griffin lab slide scanner and exporting as .OME.tiff files. The OME format includes resolution metadata, and I have a script that uses this information to guess the diameter of the myofibers for cellpose segmentation. If you don't export in OME format, you will have to adjust the diameter parameter in the slurm script. Regardless of the objective lens you use, the pixel resolution parameter should automatically be used to calculate the intended myofiber diameter. 

First, you will need to upload your data to Rivanna. You can do this through the OpenOnDemand web browser, or a terminal file transfer program like scp. There is one reccomended way to structure your files:
- my_data_dir (any name is acceptable. Your study abbreviation, for example)
    - original_images (.ome.tiff images go here)
    - fiber_masks (will be populated with .png masks after segmentation)
        - log (records of error and output messages for each file)

## Preinstalled cellpose use instructions (easier method)
This method leverages the modules installed to Rivanna and doesn't require any environment changes. All that is necessary is to download the code from this repository that will execute those modules for you. 

#### Brief setup:
1. Open a terminal on Rivanna
2. Navigate to your scratch directory: `cd /scratch/<your_user_id>`
3. Clone this repo to have the necessary code: `git clone https://github.com/mrariden/rivanna_cellpose.git`

#### Running cellpose with a single image file: 
1. Open a terminal on Rivanna
2. Run cellpose: `sbatch /scratch/<your_user_id>/fiber_seg_CLI_OME-model_rvcp-modules.slurm /path/to/your/image/file /path/to/output/directory`
    - Nothing will be saved if you do not provide an output directory.
    - A `log` directory will be created in the provided output directory and populated with error and output logs. 
    - A convenient way to not type out the output directory is to navigate (`cd`) to the intended output directory and use the `pwd` command like this: `sbatch /scratch/<your_user_id>/fiber_seg_CLI_OME-model_rvcp-modules.slurm /path/to/your/image/file $(pwd)`
    
#### Running cellpose with a folder of image files:
1. Open a terminal on Rivanna
2. Navigate to your project directory where your files are stored, (inside of 'my_data_dir').
3. Run the `segment_remaining.py` script: `python3 /scratch/<your_user_id>/rivanna_cellpose/segment_remaining.py $(pwd)`
    - This will search the `original_images` directory and will segment each image if there is no matching mask file in the `fiber_masks` directory. 
    - Each image is submitted as a seperate slurm job. Each file individually runs the slurm script above if the mask file is not found.
    - This command can be run as many times as is need if jobs don't finish for what ever reason (commonly out-of-memory, OOM, errors). 
    - You can check the number of files in each directory (the original files and mask files) with `ls -l <my_directory> | wc -l`, and comparing the number of files in each of `original_images` and `fiber_masks` (note that `fiber_masks` will contain a `log` directory and will have an extra file due to that. 
    - Log files are located in the `fiber_masks/log` directory.

## Local installation instructions (harder method)

### Anaconda is not available on Rivanna
Instead, the raw miniforge conda distribution will have to be used to isolate the cellpose insatllation environment. Follow these steps: 

#### Cellpose insatallation on Rivanna using miniforge conda
1. Navigate to a terminal on Rivanna
2. Load the miniforge conda: `module load miniforge`. the `conda` command will now work. You could adjust the .conda_envs location, which will default to the /home/\<userid> directory. It is fine to leave it pointing to home
3. Create a cellpose environment: `conda create -n cellpose python=3.9`. python 3.9 works at the time of writing, later versions may be necessary in the future. Also the name of the environment, 'cellpose' here, is completely up to you to pick.  
4. Activate the environment: `conda activate cellpose`
5. Install cellpose & pytorch GPU libraries (the GUI components aren't necessary): `pip install cellpose torch torchvision`. This will likely take a while, it took me ~30 minutes. Go get a coffee. 

Cellpose is now installed using conda. Everytime you log in to Rivanna you will need to load the miniforge conda and then activate the cellpose environment (steps 2 & 4). 

### Rivanna LAD staining segmentation workflow
The following pieces are required for this workflow to run: 
1. The slurm script
2. The segment_remaining.py script
3. Your data organized as follows:

- my_data_dir
    - original_images (.ome.tiff images go here)
    - fiber_masks
        - log
    - segment_remaining.py
    
Adjust your directory structure to conform to this. Error and output logs will be saved in the log directory. 

#### Monitoring SLURM jobs
Jobs can be monitored with the `squeue` command. A useful flag is the `-u` user flag which will only show you the jobs that you have submitted. So, if your userID is ab1cd, you can monitor your jobs with `squeue -u ab1cd`. 

### SLURM script details
- SBATCH settings: These are the basic settings that allocate resources to run a slurm job. They are defined at the top of every .slurm file. They define things like the partition (to use gpu cores, or 'standard' cpu cores), the job run time before exipring, the amount of RAM memory, and the allocation. The allocation specifies which account the computing resources are deducted from. 

The `--gres` setting changes the GPU hardware that is requested for the job. As Rivanna's hardware options change this may need to be adjusted. It is currently set to use

The Rivanna engineering team made a script generator to help adjust these settings, [available here](https://www.rc.virginia.edu/userinfo/hpc/slurm-script-generator/). 
