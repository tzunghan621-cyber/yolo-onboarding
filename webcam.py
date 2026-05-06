import time
import cv2
from ultralytics import YOLO

MODEL = "weights/yolo11n.pt"
CONF = 0.4
CAM_INDEX = 0

model = YOLO(MODEL)
cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit(f"Cannot open camera index {CAM_INDEX}")

prev = time.time()
while True:
    ok, frame = cap.read()
    if not ok:
        break

    results = model.predict(frame, verbose=False, conf=CONF)
    annotated = results[0].plot()

    now = time.time()
    fps = 1.0 / max(now - prev, 1e-6)
    prev = now
    cv2.putText(
        annotated, f"FPS: {fps:.1f}  conf>={CONF}",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
    )

    cv2.imshow("YOLO11n  (q to quit)", annotated)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
