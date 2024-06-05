# User Manual for In-VERSE

## Table of Contents
1. Introduction
2. Installation
3. Usage
4. Troubleshooting
5. Contributing
6. License
7. Acknowledgements

---

## 1. Introduction

**In-VERSE** is a final year project designed to create panoramic images from a set of input images and visualize them in a 3D layout. This tool enables users to stitch multiple images to form a panorama and then convert it into a 3D model that can be viewed and manipulated. It is built using Python, leveraging libraries such as OpenCV, Flask, and Open3D.

---

## 2. Installation

### Prerequisites
- Python 3.9.19
- Conda environment manager
- Git
- Bash shell (for running shell scripts)

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/vectoraico/In-VERSE.git
    cd In-VERSE
    ```

2. **Create a conda environment:**
    ```bash
    conda create -n inverse-env python=3.9.19
    conda activate inverse-env
    ```

3. **Install required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

### Required Libraries

```plaintext
opencv-contrib-python==4.9.0.80
opencv-python==4.9.0.80
imageio==2.19.2
pillow==10.2.0
fastapi==0.110.0
flask==3.0.2
uvicorn==0.29.0
numpy==1.24.4
pandas==2.2.1
scikit-learn==1.4.1.post1
scipy==1.8.1
torch==2.2.1
torchvision==0.17.1
matplotlib==3.8.3
plotly==5.20.0
requests==2.31.0
tqdm==4.66.2
open3d==0.17.0
```

---

## 3. Usage

### Running the Application

1. **Prepare the Images:**

   Place 4-8 images in the `Stitching/data/${folder_name}/` directory. Ensure the images are appropriately named and ordered.

2. **Run the Main Script:**

    ```bash
    python Stitching/main.py -i Stitching/data/${folder_name} -o ${panorama_name}
    ```

    This command stitches the images into a panorama and saves it in `HorizonNet/assets/`.

3. **Execute the Shell Script:**

    Run the following shell script to process the panorama and create a 3D model:

    ```bash
    ./run.sh ${panorama_name}.jpg
    ```

    The processed 3D model will be saved in `In-VERSE/static/models/`.

4. **Configure the Backend:**

    After placing all the property images from `Stitching/data/${folder_name}` into `In-VERSE/static/images/${folder_name}`, edit the `app.py` file in the `In-VERSE` directory to update the property data:

    ```python
    @app.route('/house/<int:property_id>')
    def house(property_id):
        property_data = dict(pd.read_csv("./data/PropertyInfo.csv", index_col="id").iloc[property_id])
        property_data["image_gallery"] = []
        models = {
            0:"${property1}",
            1:"${property2}",
            2:"${property3}",
            3:"${property4}"
        }
        for root, _, files in os.walk(f"static/images/{property_id}"):
            for file in files:
                if file != ".DS_Store":
                    file_path = os.path.join("/".join(root.split('/')[1:]), file)
                    property_data["image_gallery"].append(file_path)
    ```

5. **Run the Flask Application:**

    Navigate to the `In-VERSE/In-VERSE` directory and run the Flask app:

    ```bash
    flask run
    ```

    Alternatively:

    ```bash
    python app.py
    ```

6. **Access the Front End:**

    Open the link provided by Flask in your browser to access the front end. Here, you can browse properties, view the 3D models, and submit new properties with images.

---

## 4. Troubleshooting

### Common Issues

1. **Missing Images:**
    - Ensure that 4-8 images are placed in the correct directory (`data/folder_name/`).

2. **Dependencies:**
    - Make sure all required libraries are installed. Use `pip install -r requirements.txt` to install any missing dependencies.

3. **Script Execution:**
    - Ensure that the shell script `run.sh` is executable. You might need to set the execute permission:
      ```bash
      chmod +x run.sh
      ```

4. **Flask Server:**
    - If the Flask server does not start, check for port conflicts or missing dependencies.

---

## 5. Contributing

### How to Contribute

1. **Fork the repository:**
    - Go to the project repository and click the "Fork" button.

2. **Create a new branch:**
    - Create a new branch for your feature or bugfix.
      ```bash
      git checkout -b my-feature-branch
      ```

3. **Make your changes:**
    - Implement your feature or bugfix.

4. **Commit your changes:**
    - Commit your changes with a meaningful message.
      ```bash
      git commit -m "Description of my changes"
      ```

5. **Push to your fork:**
    - Push your changes to your forked repository.
      ```bash
      git push origin my-feature-branch
      ```

6. **Submit a pull request:**
    - Go to the original repository and submit a pull request.

---

## 6. License

**In-VERSE** is licensed under the MIT License. See the LICENSE file for more details.

---

## 7. Acknowledgements

- OpenCV for image processing
- FastAPI and Flask for the web framework
- Open3D for 3D model visualization
- Contributors and collaborators who helped with the project

---

By following this manual, you should be able to set up, run, and contribute to the **In-VERSE** project successfully. If you encounter any issues not covered in this manual, please refer to the project's repository for more details or contact the maintainers.

