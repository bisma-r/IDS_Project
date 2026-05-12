"""
02_extract_features.py
-----------------------
For every event in the index (data/event_index.csv):
  1. Extracts a ±WINDOW_SEC frame window around the event timestamp.
  2. Runs YOLOv8 on each frame to detect players and the ball.
  3. Computes 14 hand-crafted spatial / temporal features per event window.
  4. Saves the resulting feature matrix to data/features.csv.

Requirements:
    pip install ultralytics opencv-python numpy pandas tqdm
"""

import cv2
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from utils import (
    load_model,
    detect_objects,
    compute_features,
    WINDOW_SEC,
    FRAME_SKIP,
)

# ── CONFIG ─────────────────────────────────────────────────────────────────────
EVENT_INDEX = Path("data/event_index.csv")
OUTPUT_CSV  = Path("data/features.csv")
# ───────────────────────────────────────────────────────────────────────────────


def extract_frames(video_path: str, position_sec: float, window: int = WINDOW_SEC):
    """
    Returns a list of BGR frames in the [position_sec - window, position_sec + window]
    range, sampled every FRAME_SKIP frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    start_frame = max(0, int((position_sec - window) * fps))
    end_frame   = int((position_sec + window) * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frames = []
    frame_idx = start_frame

    while frame_idx <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        if (frame_idx - start_frame) % FRAME_SKIP == 0:
            frames.append(frame)
        frame_idx += 1

    cap.release()
    return frames

def main():
    index = pd.read_csv(EVENT_INDEX)
    index = index[index["video_exists"] == True].reset_index(drop=True)

    # ── Resume support: skip already-processed events ──────────────────
    if OUTPUT_CSV.exists():
        already_done = pd.read_csv(OUTPUT_CSV)
        print(f"Resuming — {len(already_done)} events already processed, skipping them.")
        index = index.iloc[len(already_done):].reset_index(drop=True)
    else:
        already_done = None
    # ───────────────────────────────────────────────────────────────────

    print(f"Processing {len(index)} remaining events...")
    model = load_model()

    for _, row in tqdm(index.iterrows(), total=len(index), desc="Extracting features"):
        video_path   = row["video_path"]
        position_sec = float(row["position_sec"])
        label        = row["label"]

        frames = extract_frames(video_path, position_sec)
        if len(frames) < 2:
            continue

        detections = detect_objects(model, frames)
        features   = compute_features(frames, detections)
        features["label"] = label

        # ── Save after every single event ──────────────────────────────
        row_df = pd.DataFrame([features])
        write_header = not OUTPUT_CSV.exists()
        row_df.to_csv(OUTPUT_CSV, mode="a", header=write_header, index=False)
        # ───────────────────────────────────────────────────────────────

    print(f"\nDone. Features saved to: {OUTPUT_CSV}")
    print(pd.read_csv(OUTPUT_CSV)["label"].value_counts())

if __name__ == "__main__":
    main()