from ultralytics import YOLO
import os
import matplotlib.pyplot as plt
import cv2

# Load trained model
model = YOLO("runs/detect/civic_v12/weights/best.pt")

# Run inference
results = model.predict(
    source="p3.jpg",
    conf=0.25,
    save=True,
    show=False
)

# Get saved image path
save_dir = results[0].save_dir
img_name = os.path.basename(results[0].path)
output_path = os.path.join(save_dir, img_name)

print("Showing result from:", output_path)

# Read image
img = cv2.imread(output_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Show image (BLOCKS until window closed)
plt.imshow(img)
plt.title("YOLO Detection Result")
plt.axis("off")
plt.show()   # 👈 stays open until YOU close it
