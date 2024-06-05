import os
import cv2
import yaml
from PIL import Image
from stitching import Stitcher

def load_stitching_parameters(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['stitching_parameters']

def list_files(input_folder):
    files = os.listdir(input_folder)
    imgs = []
    for f in files:
        if f == ".DS_Store": continue
        if os.path.isfile(os.path.join(input_folder, f)):
            imgs.append(os.path.join(input_folder, f))
    # return [os.path.join(input_folder, file) for file in files]
    return imgs

def stitch_panorama(input_folder, output_name, config_file="configs/stitching_config.yaml"):
    # Load stitching parameters from YAML config file
    stitching_parameters = load_stitching_parameters(config_file)

    # Initialize the Stitcher with the parameters
    stitcher = Stitcher(**stitching_parameters)

    # List all files in the input folder
    image_paths = list_files(input_folder)

    # Stitch images
    panorama = stitcher.stitch(image_paths)

    # Convert and save panorama
    panorama = cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(panorama)
    out_path = f"output/{output_name}.jpg"
    image.save(out_path)

    return out_path
