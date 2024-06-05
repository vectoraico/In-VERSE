# Panorama Stitcher

Panorama Stitcher is a Python tool for stitching multiple images together to create a panoramic view and adding 360-degree metadata to the resulting image.

## Features

- Stitch multiple images to create a panoramic view.
- Add 360-degree metadata to the stitched panorama image.
- Configurable stitching parameters via YAML configuration files.
- Command-line interface for easy usage.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/panorama-stitcher.git
   ```

2. Navigate to the project directory:

   ```bash
   cd FYP
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To stitch images and add 360-degree metadata, follow these steps:

1. Prepare your input images in a directory.
2. Run the `main.py` script with appropriate command-line arguments:

   ```bash
   python main.py -i path/to/input/folder -o output_panorama_name
   ```

   Optional arguments:

   - `-i, --input-folder`: Path to the input image folder (default: "data/office").
   - `-o, --output-name`: Name of the output panorama image (default: "panorama").
   - `-c, --config-file`: Path to the configuration file (default: "configs/stitching_config.yaml").

3. The stitched panorama image with 360-degree metadata will be saved in the `output` directory.

## Configuration

Stitching parameters can be configured using YAML files. Edit the `stitching_config.yaml` file in the `configs` directory to customize the stitching process.
