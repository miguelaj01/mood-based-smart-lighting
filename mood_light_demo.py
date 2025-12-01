"""
Mood-Based Smart Lighting System (Screen Only Version)
------------------------------------------------------

Uses webcam + FER to detect facial emotions in real-time.
Loads a CSV dataset mapping emotions to moods and colors.
Displays an on-screen "Mood Light" panel that changes color.
"""

import cv2
import numpy as np
from fer.fer import FER
from collections import deque
import csv

SMOOTHING_WINDOW = 10
CSV_PATH = "mood_color_mapping.csv"

def load_mood_mapping(csv_path):
    mapping = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emotion = row["emotion"].strip().lower()
            r, g, b = int(row["r"]), int(row["g"]), int(row["b"])
            mapping[emotion] = {
                "mood": row["mood"].strip(),
                "color_name": row["color_name"].strip(),
                "rgb": (r, g, b),
                "bgr": (b, g, r),
            }
    return mapping

print("[INFO] Loading mood-color dataset...")
MOOD_DATASET = load_mood_mapping(CSV_PATH)
print("[INFO] Dataset loaded successfully.")

def get_color_for_emotion(emotion):
    if not emotion:
        return (255, 255, 255)
    info = MOOD_DATASET.get(emotion.lower())
    if info:
        return info["bgr"]
    return (255, 255, 255)

def get_color_label_for_emotion(emotion):
    if not emotion:
        return "Neutral"
    info = MOOD_DATASET.get(emotion.lower())
    if info:
        return info["color_name"]
    return emotion

def get_dominant_emotion(detector, frame):
    result = detector.top_emotion(frame)
    if result is None:
        return None, 0.0
    emotion, score = result
    return emotion, score

def smooth_emotion(history, new_emotion):
    if new_emotion:
        history.append(new_emotion)
    if not history:
        return None
    return max(set(history), key=history.count)

def main():
    cap = cv2.VideoCapture(0)
    detector = FER(mtcnn=True)
    history = deque(maxlen=SMOOTHING_WINDOW)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[INFO] Starting Mood Light Demo (Screen Only)")
    print("       Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read from camera.")
            break

        frame = cv2.flip(frame, 1)

        raw_emotion, score = get_dominant_emotion(detector, frame)

        if score is None:
            score = 0.0

        smoothed = smooth_emotion(history, raw_emotion)
        mood = smoothed or "neutral"

        color_bgr = get_color_for_emotion(mood)
        color_label = get_color_label_for_emotion(mood)

        status = f"Detected: {raw_emotion or 'None'} ({float(score):.2f}) | Mood: {mood}"
        cv2.putText(frame, status, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Camera Feed - Emotion Detection", frame)

        panel = np.zeros((300, 300, 3), dtype=np.uint8)
        panel[:] = color_bgr

        cv2.putText(panel, color_label.upper(), (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(panel, f"({mood.upper()})", (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        cv2.imshow("Mood Light (Screen Preview)", panel)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
