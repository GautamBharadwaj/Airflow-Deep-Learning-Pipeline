import os
import glob
import numpy as np
import pickle
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

class GenerateObjectEmbedding:
    def __init__(self, dataset_path, embeddings_output_path):
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')  # Pretrained ResNet
        self.image_size = (224, 224)  # Resize images to fit ResNet input
        self.dataset_path = dataset_path
        self.embeddings_output_path = embeddings_output_path

    def genObjectEmbedding(self):
        imagePaths = glob.glob(os.path.join(self.dataset_path, "*.jpg"))  # Adjust the extension if needed
        knownEmbeddings = []
        knownNames = []
        total = 0
        for (i, imagePath) in enumerate(imagePaths):
            name = os.path.splitext(os.path.basename(imagePath))[0]
            img = image.load_img(imagePath, target_size=self.image_size)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            embedding = self.model.predict(img_array)
            embedding = embedding.flatten()
            knownNames.append(name)
            knownEmbeddings.append(embedding)
            total += 1
        data = {"embeddings": knownEmbeddings, "names": knownNames}
        with open(self.embeddings_output_path, "wb") as f:
            pickle.dump(data, f)
