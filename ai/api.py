from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2
import tempfile
import os


app = FastAPI()


model = YOLO("runs/detect/civic_v12/weights/best.pt")
print("✅ Model loaded successfully")


@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(await file.read())
        input_image_path = temp.name

    
    image = cv2.imread(input_image_path)

    
    results = model(image)

    detections = []

    
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            label = f"{model.names[cls_id]} {confidence:.2f}"

            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            detections.append({
                "class": model.names[cls_id],
                "confidence": round(confidence, 2),
                "bbox": [x1, y1, x2, y2]
            })


    output_image_path = input_image_path.replace(".jpg", "_detected.jpg")
    cv2.imwrite(output_image_path, image)

    
    os.remove(input_image_path)

    
    return {
        "detections": detections,
        "detected_image_path": output_image_path
    }
