import os
import pickle
import urllib.request
import tarfile
from glob import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Download and extract dataset if not already present
dataset_dir = "../dataset"
os.makedirs(dataset_dir, exist_ok=True)
tar_path = os.path.join(dataset_dir, "aclImdb_v1.tar.gz")
extracted_dir = os.path.join(dataset_dir, "aclImdb_downloaded")

if not os.path.exists(extracted_dir):
    print("Downloading dataset...")
    urllib.request.urlretrieve("https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz", tar_path)
    print("Extracting dataset...")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(extracted_dir)
    os.remove(tar_path)  # Clean up the tar file

# load data from train folder
texts = []
labels = []

# load negative reviews (label = 0)
neg_path = os.path.join(extracted_dir, "aclImdb", "train", "neg")
for file in glob(os.path.join(neg_path, "*.txt")):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        texts.append(f.read())
        labels.append(0)

# load positive reviews (label = 1)
pos_path = os.path.join(extracted_dir, "aclImdb", "train", "pos")
for file in glob(os.path.join(pos_path, "*.txt")):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        texts.append(f.read())
        labels.append(1)

print(f"Loaded {len(texts)} reviews")

# vectorize text
print("Vectorizing text...")
vectorizer = TfidfVectorizer(max_features=5000)
X_vec = vectorizer.fit_transform(texts)

# train model
print("Training model...")
model = LogisticRegression(max_iter=1000)
model.fit(X_vec, labels)

# save model
os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("Model trained and saved successfully")