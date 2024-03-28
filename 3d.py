import pickle
import cv2
import argparse
from visualization.obj3d import create_3d_obj

def visualize_3d_from_pkl(pkl_file_path):
    # Load the data using pickle
    with open(pkl_file_path, 'rb') as f:
        loaded_data = pickle.load(f)

    dt_boundaries = loaded_data['dt_boundaries']
    dt_layout_depth = loaded_data['dt_layout_depth']
    img = loaded_data['img']
    save_path = loaded_data['save_path']

    create_3d_obj(cv2.resize(img, dt_layout_depth.shape[::-1]), dt_layout_depth,
                    save_path=save_path, mesh=True,  show=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize 3D from .pkl file")
    parser.add_argument("-p", "--pkl_path", type=str, required=True, help="Path to the .pkl file")
    args = parser.parse_args()
    visualize_3d_from_pkl(args.pkl_path)
