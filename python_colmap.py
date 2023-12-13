import pathlib
import pycolmap
import numpy as np
import cv2
import matplotlib.pyplot as plt
from IPython.display import display, Image

# Function to visualize images
def display_images(image_paths):
    for path in image_paths:
        display(Image(filename=str(path)))

# Function to visualize SIFT features
def visualize_sift_features(database_path, num_images=3):
    # Load the database
    database = pycolmap.read_database(database_path)

    # Randomly select images for visualization
    selected_image_ids = np.random.choice(list(database['images'].keys()), num_images, replace=False)

    for image_id in selected_image_ids:
        image = database['images'][image_id]
        keypoints = image['point2D']

        img = cv2.imread(str(image['name']))

        # Draw SIFT features on the image
        img_with_sift = cv2.drawKeypoints(
            img,
            [cv2.KeyPoint(x=k[0], y=k[1], _size=k[2], _angle=k[3], _response=k[4], _octave=k[5], _class_id=k[6]) for k in keypoints],
            None,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )

        plt.imshow(cv2.cvtColor(img_with_sift, cv2.COLOR_BGR2RGB))
        plt.title(f"SIFT Features - Image {image_id}")
        plt.axis('off')
        plt.show()

# Function to visualize 3D reconstruction
def visualize_3d_reconstruction(reconstruction_path):
    colmap_path = pathlib.Path("./mvs")
    !{colmap_path / 'gui'} {reconstruction_path}

# Function to reconstruct with options and visualize at each step
def reconstruct_with_options_and_visualize(image_folder, output_path):
    # Extract features
    database_path = output_path / "database.db"
    pycolmap.extract_features(
        database_path,
        image_folder,
        sift_options={"max_num_features": 10000, "first_octave": -1, "num_octaves": 5}
    )
    
    # Visualize extracted features on random images
    visualize_sift_features(database_path)

    # Match features
    pycolmap.match_exhaustive(
        database_path,
        matching_options={"SiftMatchingOptions": {"max_num_matches": 32768, "lowes_ratio": 0.8}}
    )

    # Incremental reconstruction
    maps = pycolmap.incremental_mapping(
        database_path,
        image_folder,
        output_path,
        mapper_options={"MapperOptions": {"extract_colors": True}}
    )

    # Visualize sparse reconstruction
    visualize_3d_reconstruction(output_path / "sparse/0")

    # Dense reconstruction
    mvs_path = output_path / "mvs"
    pycolmap.undistort_images(mvs_path, output_path, image_folder)

    # Optional: Increase max_gcp_distance for better dense reconstruction results
    # Uses CUDA
    pycolmap.patch_match_stereo(mvs_path, {"PatchMatchStereoOptions": {"max_gcp_distance": 60}})
    pycolmap.stereo_fusion(mvs_path / "dense.ply", mvs_path)

    # Visualize dense reconstruction (optional)
    visualize_3d_reconstruction(mvs_path / "dense.ply")

if __name__ == '__main__':
    image_folder = pathlib.Path("./image_folder")
    output_path = pathlib.Path("./output_path")
    
    reconstruct_with_options_and_visualize(image_folder, output_path)
    
