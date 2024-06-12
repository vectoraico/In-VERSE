import warnings
warnings.filterwarnings("ignore")

import os
import sys
import argparse
import subprocess
import pandas as pd
sys.path.append("../Stitching")
sys.path.append("../ErrorDetection")
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = "./data/PropertyInfo.csv"
# Append the base directory to the system path
sys.path.append(base_path)
from Stitching.src import stitch_panorama, add_360_metadata
from ErrorChecking.guardrails import allowed_file
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/add_property")
def add_property():
    return render_template('property_details.html')

@app.route('/submit', methods=['POST'])
def submit_property():
    property_data = pd.read_csv(DATA_PATH)
    id = len(property_data)
    property_name = request.form['property_name']
    location = request.form['location']
    property_type = request.form['property_type']
    num_rooms = request.form['num_rooms']
    size = request.form['size']
    price = request.form['price']
    email = request.form['email']
    description = request.form['description']
    num_bathrooms = request.form['num_bathrooms']
    amenities = request.form['amenities']
    agent_name = request.form['agent_name']
    phone = request.form['phone']
    website = request.form['website']

    photos = request.files.getlist('photos')

    folder = os.path.join('./static/images', str(id))
    os.makedirs(folder, exist_ok=True)
    
    for file, photo in enumerate(photos):
        if photo:
            filename = os.path.join(folder, "1_"+str(file+1)) + ".jpg"
            photo.save(filename) 

    for image in os.listdir(folder):
        if allowed_file(os.path.join(folder, image)):
            return "Images are not acceptable. \
                    Image must be sharp and a single object can't cover more than 30% of the image area."
        
    # Integrating Stitching Pipeline
    out_path = './static/images/original/'
    out_name = str(id)+"_1"
    path = os.path.join(out_path, out_name+".jpg")
    stitch_panorama(input_folder=folder, output_name=out_name, out_path=out_path)
    add_360_metadata(path)

    curr_path = os.getcwd()
    os.chdir('..')

    path = f"./In-VERSE{path[1:]}"
    subprocess.run(["bash", "run.sh", path])

    os.chdir(curr_path)
    new_property = pd.DataFrame([{
        'id': id,
        'room_id': 1,
        'property_name': property_name,
        'description': description,
        'location': location,
        'property_type': property_type,
        'num_rooms': num_rooms,
        'num_bathrooms': num_bathrooms,
        'size': size,
        'amenities': amenities,
        'price': price,
        'agent_name': agent_name,
        'phone': phone,
        'email': email,
        'website': website,
        'image_gallery': []
    }])

    # Append the new property to the existing property data
    property_data = pd.concat([property_data, new_property])

    # Save the updated property data back to the CSV file
    property_data.to_csv(DATA_PATH, index=False)

    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/property/<int:property_id>/<int:room_id>', methods=["GET"])
def property(property_id, room_id):
    property_data = pd.read_csv(DATA_PATH)
    property_data = property_data[property_data["id"] == property_id]
    rooms = len(property_data)
    property_data = property_data[property_data["room_id"] == room_id]
    property_data = property_data.iloc[0].to_dict()
    property_data["rooms"] = rooms
    property_data["image_gallery"] = []
    models = {
        0: "office_developer",
        1: "landkrafts",
        2: "class1",
        3: "audi1"
    }
    for root, _, files in os.walk(f"static/images/{property_id}"):
        for file in files:
            if file != ".DS_Store":
                file_path = os.path.join("/".join(root.split('/')[1:]), file)
                property_data["image_gallery"].append(file_path)
    # property_data["model"] = models[int(property_id)]
    property_data["model"] = str(property_data["id"]) + "_" + str(property_data["room_id"])


    if property_data:
        return render_template('property.html', **property_data)
    else:
        return "Property not found", 404

@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download_pano/<string:property_id>',methods = ["GET"])
def pano(property_id):
    directory = 'static/images/original'
    filename=f"{property_id}.jpg"
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/model/<string:model_name>')
def showmodel(model_name):
    num_geometries = 2 # Example value
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