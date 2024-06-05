import sys
import open3d as o3d

def load_geometries(img_file, num_geometries):
    loaded_geometries = []
    for i in range(num_geometries):
        try:
            mesh = o3d.io.read_triangle_mesh(f"static/models/output/{img_file}_geometry_{i}.ply")
            loaded_geometries.append(mesh)
        except:
            try:
                lines = o3d.io.read_line_set(f"static/models/output/{img_file}_geometry_{i}.ply")
                loaded_geometries.append(lines)
            except:
                print(f"Failed to load {img_file}_geometry_{i}.ply")
    return loaded_geometries

def visualize_geometries(geometries):
    o3d.visualization.draw_geometries(geometries,  mesh_show_back_face=True)
    
if __name__ == "__main__":
    # Example usage: python visualize.py model_name num_geometries
    model_name = sys.argv[1]
    num_geometries = int(sys.argv[2])
    geometries = load_geometries(model_name, num_geometries)
    visualize_geometries(geometries)