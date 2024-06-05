from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os
import argparse
import subprocess
    
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
        2:"class2",
        3:"audi1"
    }
    for root, _, files in os.walk(f"static/images/{property_id}"):
        for file in files:
            if file != ".DS_Store":
                file_path = os.path.join("/".join(root.split('/')[1:]), file)
                property_data["image_gallery"].append(file_path)
    print(property_data["image_gallery"])
    property_data["model"] = models[int(property_id)]
    property_data["id"] = property_id
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

@app.route('/download_pano/<int:property_id>',methods = ["GET"])
def pano(property_id):
    print(property_id)
    directory = 'static/images/original'
    filename=f"{property_id}.jpg"
    return send_from_directory(directory, filename, as_attachment=True)

# @app.route('/render')
# def render():
#     # path = f"../static/models/output/{path}_geometry_0.ply"
#     return render_template('render.html')

@app.route('/model/<string:model_name>')
def showmodel(model_name):
    num_geometries = 2 # Example value
    # Call the visualize.py script with the model name and number of geometries as arguments
    subprocess.run(["python", "visualise.py", model_name, str(num_geometries)])
    return render_template("price.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True, port=8000)
