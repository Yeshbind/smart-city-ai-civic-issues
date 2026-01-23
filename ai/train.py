from ultralytics import YOLO

# Load pretrained YOLOv8 nano model
model = YOLO("yolov8n.pt")

# Train
model.train(
    data="MainDataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    device=0,      # GPU (RTX 4050)
    workers=0,     # IMPORTANT on Windows
    name="civic_v1"
)




