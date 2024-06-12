import os
import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader



def blur_detect_ML(image_path):
    class FeatureExtractor(nn.Module):
        def __init__(self):
            super(FeatureExtractor, self).__init__()
            self.resnet = models.resnet18(pretrained=True)
            self.resnet.fc = nn.Identity() 
    
        def forward(self, x):
            return self.resnet(x)
    
    #Setting up a shallow Fully Connected Classifier
    class Classifier(nn.Module):
        def __init__(self, input_size, num_classes):
            super(Classifier, self).__init__()
            self.fc1 = nn.Linear(input_size, 128)
            self.fc2 = nn.Linear(128, num_classes)
    
        def forward(self, x):
            x = torch.flatten(x, 1)  # Flatten the features
            x = nn.functional.relu(self.fc1(x))
            x = self.fc2(x)
            return x
    
    feature_extractor = FeatureExtractor()
    classifier = Classifier(512, 3)
    model = nn.Sequential(feature_extractor, classifier)
    
    #Loading our trained model
    model.load_state_dict(torch.load('../ErrorChecking/BlurDetection/model.pth'))
    model.eval()
    
    #Defining an inference method for custom images
    def classify_image(image_path, model):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        image = transform(Image.open(image_path)).unsqueeze(0)
        features = feature_extractor(image[:,:3,:])
        outputs = classifier(features)
        _, predicted = torch.max(outputs.data, 1)
        return predicted.item()
    
    #Mapping the class index - To Category
    category = {0: "blur", 1: "blur", 2: "sharp"}
    # image_path = 'img1.jpeg'
    
    class_index = classify_image(image_path, model)
    return category[class_index]


def calculate_laplacian_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def blur_detect_DIP(image_path):

    image = cv2.imread(image_path)

    threshhold = 100
    laplacian_var = calculate_laplacian_variance(image)
    
    if laplacian_var < threshhold:
        return False
    else:
        return True
    
def detect_blur(image_path):
    DIP = blur_detect_DIP(image_path)
    ML = blur_detect_ML(image_path)

    if (DIP == "sharp" and ML == "sharp"):
        return True

    if (DIP == "blur" and ML == "blur"):
        return False

    return False

#Laoding a YOLO v3 - Pretrained Model
def reject_majority(image):
    net = cv2.dnn.readNet("../ErrorChecking/ObjectDetection/yolov3/yolov3.weights", "../ErrorChecking/ObjectDetection/yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    
    #loading names of the classes from Microsoft COCO Dataset
    with open("./ObjectDetection/coco.names", "r") as f:
        classes = [line.strip() for line in f]
    
    #Take the input image
    height, width, _ = image.shape
    total_area = height * width
    
    #Detectht the objects
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    flag = False
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
    
            #Compute Area taken
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                area = w * h
                
                if area / total_area > 0.3:  # checking if the 30% of the image area contains a single object reject it.
                    flag = True
    
    return not flag


def allowed_file(image_path):
    image = cv2.imread(image_path)
    return detect_blur(image_path) and reject_majority(image)



if __name__ == "__main__":
    image_path = "/Users/abdulwadood/Downloads/Archive 2/FYP Final/ErrorChecking/BlurDetection/img1.jpeg"
    print(allowed_file(image_path))