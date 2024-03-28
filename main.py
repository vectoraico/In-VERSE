import argparse
from src import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Stitch images to create a panorama")
    parser.add_argument("-i", "--input-folder", type=str, required=True, help="Path to input image folder")
    parser.add_argument("-o", "--output-name", type=str, default="panorama", help="Name of the output panorama image")
    parser.add_argument("-c", "--config-file", type=str, default="configs/stitching_config.yaml", help="Path to the configuration file")
    args = parser.parse_args()

    # Stitch panorama
    path = stitch_panorama(args.input_folder, args.output_name, args.config_file)

    add_360_metadata(path)

