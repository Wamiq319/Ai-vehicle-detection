from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("best.pt")  # path to your trained 6-class vehicle model

charged_ids = set()  # store IDs we’ve already billed

# Track video
for result in model.track(
        source="v1.mp4",                # or 0 for webcam
        tracker="bytetrack.yaml",
        stream=True,
        conf=0.5,
        classes=[0, 1, 2, 3, 4, 5]      # your 6 vehicle classes
    ):

    frame = result.plot()

    # ✅ Skip frames with no detections
    if result.boxes is None or result.boxes.id is None:
        cv2.imshow("Toll Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Loop through all detected and tracked vehicles
    for box, track_id, cls in zip(result.boxes.xyxy,
                                  result.boxes.id,
                                  result.boxes.cls):
        vid = int(track_id)
        cname = model.names[int(cls)]

        # Toll trigger only once per ID
        if vid not in charged_ids:
            charged_ids.add(vid)
            print(f"TOLL EVENT: ID={vid}, class={cname}")
            # Example: send_toll_event(vid, cname)

    # Display the processed frame
    cv2.imshow("Toll Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("best.pt")  # path to your trained 6-class vehicle model

charged_ids = set()  # store IDs we’ve already billed

# Track video
for result in model.track(
        source="v1.mp4",                # or 0 for webcam
        tracker="bytetrack.yaml",
        stream=True,
        conf=0.5,
        classes=[0, 1, 2, 3, 4, 5]      # your 6 vehicle classes
    ):

    frame = result.plot()

    # ✅ Skip frames with no detections
    if result.boxes is None or result.boxes.id is None:
        cv2.imshow("Toll Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Loop through all detected and tracked vehicles
    for box, track_id, cls in zip(result.boxes.xyxy,
                                  result.boxes.id,
                                  result.boxes.cls):
        vid = int(track_id)
        cname = model.names[int(cls)]

        # Toll trigger only once per ID
        if vid not in charged_ids:
            charged_ids.add(vid)
            print(f"TOLL EVENT: ID={vid}, class={cname}")
            # Example: send_toll_event(vid, cname)

    # Display the processed frame
    cv2.imshow("Toll Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()