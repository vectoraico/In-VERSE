from flask import Flask, render_template, request
import pandas as pd
import os
import argparse
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
    o3d.visualization.draw_geometries(geometries, mesh_show_back_face=True)
    
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/house/<int:property_id>')
def house(property_id):
    property_data = dict(pd.read_csv("./data/PropertyInfo.csv", index_col="id").iloc[property_id])
    property_data["image_gallery"] = []
    models = {
        0:"office_developer",
        1:"landkrafts",
        2:"class1",
        3:"audi1"
    }
    for root, _, files in os.walk(f"static/images/{property_id}"):
        for file in files:
            if file != ".DS_Store":
                file_path = os.path.join("/".join(root.split('/')[1:]), file)
                property_data["image_gallery"].append(file_path)
    print(property_data["image_gallery"])
    property_data["model"] = models[int(property_id)]
    # property_data["html"] = ""
    # for i in property_data["image_gallery"]:
    #     property_data["html"] += f'<div class = "slider-images"><img src="../static/{i}"></div>'
    # print(property_data["html"])
    if property_data:
        return render_template('house.html', **property_data)
    else:
        return "Property not found", 404

@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/model/<string:model_name>')
def showmodel(model_name):
    args = {
        "img": model_name,
        "num_geometries":2
    }
    loaded_geometries = load_geometries(args["img"], args["num_geometries"])
    print(model_name)
    visualize_geometries(loaded_geometries)
    
    

@app.route('/signup')
def signup():
    return render_template('signup.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)
