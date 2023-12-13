import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import imutils

class ImageStitcher():
    
    def __init__(self,Dir_Path = "./input/office/"):
        self.path = Dir_Path
        self.img_path = sorted(os.listdir(Dir_Path), key=self._natural_sort_key)
        self.images = [cv2.imread(Dir_Path+image) for image in self.img_path]
        self.panorama = None
        
    def _natural_sort_key(self,s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

    def display_Images(self):
        fig, axes = plt.subplots(2, 3, figsize=(10, 7))
        axes = axes.flatten()

        for i in range(len(self.images)//5):
            axes[i].imshow(cv2.cvtColor(self.images[i*5], cv2.COLOR_BGR2RGB), cmap='gray') 
            axes[i].set_title(f'Image {i+1}') 

        for j in range(len(self.images), len(axes)):
            axes[j].axis('off')

        plt.tight_layout() 
        plt.show()
        
    def stitch(self):
        stitcher = cv2.Stitcher.create()
        (status, stitched) = stitcher.stitch(self.images,pano=None )
        if status == 0:
            self.panorama = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
            print("Success")
            return stitched
        else:
            print("Image stitching failed!")
            return None
        
    def crop_to_rectangle(self):
        
        thresh_img = self.get_Pano_Mask()
        # find first and last row of thresh_img to have values 
        first_row = 0
        last_row = 0

        for i in range(0,len(thresh_img)):
            # print(round(np.sum(thresh_img[i]),-3))
            if round(np.sum(thresh_img[i]),-5) == round(len(thresh_img[i])*255,-5):
                first_row = i
                break
        for i in range(len(thresh_img)-1,-1,-1):
            # print(round(np.sum(thresh_img[i]),-3))
            if round(np.sum(thresh_img[i]),-5) == round(len(thresh_img[i])*255,-5):
                last_row = i
                break
        cropped_result = self.panorama[first_row:last_row, :]
        return cropped_result

    def get_Pano_Mask(self):
        gray = cv2.cvtColor(self.panorama, cv2.COLOR_BGR2GRAY)
        thresh_img = cv2.threshold(gray, 0, 255 , cv2.THRESH_BINARY)[1]
        return thresh_img