# Import necessary libraries
from ultralytics import YOLO
import roboflow

# Initialize Roboflow with your API key
rf = roboflow.Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace().project("your-project-name")

# Load pre-trained YOLOv8s model
model = YOLO('best_hist.pt')

# Initial model training
model.train(data="path/to/initial/data.yaml", epochs=50, imgsz=640)

# Active learning loop
num_iterations = 5  # Number of active learning iterations
confidence_threshold = 0.5  # Confidence threshold to identify uncertain predictions

for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    
    # Step 2: Run inference on unlabeled data
    predictions = model.predict(source="path/to/unlabeled/images", save=True)
    
    # Step 3: Identify uncertain predictions
    uncertain_images = []
    for pred in predictions:
        if pred['confidence'] < confidence_threshold:  # Adjust threshold as needed
            uncertain_images.append(pred['image_path'])
    
    # Step 4: Upload uncertain images to Roboflow for labeling
    version = project.version(iteration + 2)  # Create a new version for each iteration
    for img_path in uncertain_images:
        version.upload(img_path)
    
    print(f"Uploaded {len(uncertain_images)} uncertain images for labeling.")
    
    # Wait for labeling to complete in Roboflow
    input("Press Enter after labeling is complete and the new version is ready for download...")
    
    # Step 5: Download labeled data from Roboflow
    dataset = project.version(iteration + 2).download("yolov8")
    
    # Step 6: Retrain the model with the new data
    model.train(data=f"/content/{dataset.location}/data.yaml", epochs=50, imgsz=640)
    
    print(f"Retrained model with updated dataset from iteration {iteration + 2}.")

print("Active learning loop completed.")
