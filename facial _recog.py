import cv2
import os
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Define emotions (modify as needed)
emotions = ["angry", "disgust", "fearful", "happy", "neutral", "sad", "surprised"]

# Load images and labels
images = []
labels = []

for emotion in emotions:
  # Replace 'path/to/emotions' with the directory containing your emotion folders
  emotion_path = f"C:/Users/saisu/OneDrive/Desktop/Hacksavvy/train/{emotion}"
  for image_file in os.listdir(emotion_path):
    image = cv2.imread(os.path.join(emotion_path, image_file))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    images.append(gray.flatten())  # Flatten image for SVM
    labels.append(emotion)

# Encode labels
le = LabelEncoder()
labels = le.fit_transform(labels)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Train SVM model
clf = SVC(kernel='linear')  # Experiment with different kernels
clf.fit(X_train, y_train)

# Save the trained model (replace with your filename)
clf.save('emotion_model.xml')

# Print training accuracy
predictions = clf.predict(X_test)
accuracy = sum(predictions == y_test) / len(y_test)
print(f"Training Accuracy: {accuracy:.2f}")
