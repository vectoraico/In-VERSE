import argparse
import open3d as o3d

def load_geometries(img_file, num_geometries):
    loaded_geometries = []
    for i in range(num_geometries):
        try:
            mesh = o3d.io.read_triangle_mesh(f"output/{img_file}_geometry_{i}.ply")
            loaded_geometries.append(mesh)
        except:
            try:
                lines = o3d.io.read_line_set(f"output/{img_file}_geometry_{i}.ply")
                loaded_geometries.append(lines)
            except:
                print(f"Failed to load {img_file}_geometry_{i}.ply")
    return loaded_geometries

def visualize_geometries(geometries):
    o3d.visualization.draw_geometries(geometries, mesh_show_back_face=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize loaded geometries from .ply files.")
    parser.add_argument("--img", type=str, help="Image file name (without extension) to load geometries.")
    parser.add_argument("--num_geometries", type=int, default=2, help="Number of geometries to load. Default is 2.")
    args = parser.parse_args()

    if args.img:
        loaded_geometries = load_geometries(args.img, args.num_geometries)
        visualize_geometries(loaded_geometries)
    else:
        print("Please provide --img argument with the image file name.")
