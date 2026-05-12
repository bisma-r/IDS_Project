"""
01_download_data.py
--------------------
Downloads SoccerNet annotation labels and video clips for the target event
classes: Penalty, Foul, Yellow card, Red card.

Requirements:
    pip install SoccerNet

Usage:
    python 01_download_data.py

Outputs:
    data/soccernet/          <- annotation JSON files per match
"""

import os
import json
from pathlib import Path

import SoccerNet
from SoccerNet.Downloader import SoccerNetDownloader
mySoccerNetDownloader=SoccerNetDownloader(LocalDirectory="C:/Users/Bisma/AppData/Roaming/Python/Python314/site-packages/SoccerNet")

mySoccerNetDownloader.password = "s0cc3rn3t"
# mySoccerNetDownloader.downloadGames(files=["1_720p.mkv", "2_720p.mkv"], split=["test"])
mySoccerNetDownloader.downloadGames(files=["Labels-v2.json"], split=["test"])


# # ── CONFIG ─────────────────────────────────────────────────────────────────────
# DATA_DIR = Path("C:/Users/Bisma/AppData/Roaming/Python/Python314/site-packages/SoccerNet")
# TARGET_CLASSES = {"Penalty", "Foul", "Yellow card", "Red card"}
# SPLITS = ["train", "valid", "test"]


# SOCCERNET_PASSWORD = "s0cc3rn3t"
# # ───────────────────────────────────────────────────────────────────────────────


# def download_annotations():
#     from SoccerNet.Downloader import SoccerNetDownloader

#     DATA_DIR.mkdir(parents=True, exist_ok=True)

#     downloader = SoccerNetDownloader(LocalDirectory=str(DATA_DIR))
#     downloader.password = SOCCERNET_PASSWORD

#     print("Downloading annotation labels...")
#     downloader.downloadGames(
#         files=["Labels-v2.json"],
#         split=SPLITS,
#         overwrite=False
#     )
#     print(f"Annotations saved to: {DATA_DIR}")


# def download_videos():

#     from SoccerNet.Downloader import SoccerNetDownloader

#     downloader = SoccerNetDownloader(LocalDirectory=str(DATA_DIR))
#     downloader.password = SOCCERNET_PASSWORD

#     print("Downloading 720p videos (this may take a while)...")
#     downloader.downloadGames(
#         files=["1_720p.mkv", "2_720p.mkv"],  # first and second halves
#         split=SPLITS,
#         overwrite=False
#     )
#     print("Videos downloaded.")


# def filter_and_summarise():

#     counts = {cls: 0 for cls in TARGET_CLASSES}
#     total_games = 0

#     for label_file in DATA_DIR.rglob("Labels-v2.json"):
#         total_games += 1
#         with open(label_file, "r") as f:
#             data = json.load(f)

#         for annotation in data.get("annotations", []):
#             label = annotation.get("label", "")
#             if label in TARGET_CLASSES:
#                 counts[label] += 1

#     print("\n── Dataset Summary ──────────────────")
#     print(f"  Total games found : {total_games}")
#     for cls, count in sorted(counts.items(), key=lambda x: -x[1]):
#         print(f"  {cls:<15}: {count} events")
#     print("─────────────────────────────────────")
#     return counts


# def build_event_index():
#     """
#     Builds a flat CSV index of all target events with their:
#     - game path
#     - half (1 or 2)
#     - position (seconds)
#     - label
#     - video path

#     Saves to data/event_index.csv
#     """
#     import csv

#     rows = []
#     for label_file in DATA_DIR.rglob("Labels-v2.json"):
#         game_dir = label_file.parent
#         with open(label_file, "r") as f:
#             data = json.load(f)

#         for ann in data.get("annotations", []):
#             label = ann.get("label", "")
#             if label not in TARGET_CLASSES:
#                 continue

#             half = int(ann.get("gameTime", "1 - 00:00").split(" - ")[0])
#             time_str = ann.get("gameTime", "1 - 00:00").split(" - ")[1]
#             mm, ss = time_str.split(":")
#             position_sec = int(mm) * 60 + int(ss)

#             video_name = f"{half}_720p.mkv"
#             video_path = game_dir / video_name

#             rows.append({
#                 "game_dir": str(game_dir),
#                 "half": half,
#                 "position_sec": position_sec,
#                 "label": label,
#                 "video_path": str(video_path),
#                 "video_exists": video_path.exists(),
#             })

#     out_path = Path("data/event_index.csv")
#     out_path.parent.mkdir(parents=True, exist_ok=True)
#     with open(out_path, "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=rows[0].keys())
#         writer.writeheader()
#         writer.writerows(rows)

#     print(f"\nEvent index saved to: {out_path}  ({len(rows)} events)")
#     return out_path


# # if __name__ == "__main__":
#     # download_annotations()
#     # download_videos()

#     # filter_and_summarise()
#     # build_event_index()

# def download_clips():
#     from SoccerNet.Downloader import SoccerNetDownloader
    
#     downloader = SoccerNetDownloader(LocalDirectory=str(DATA_DIR))
#     downloader.password = SOCCERNET_PASSWORD
    
#     # Downloads short 30-second clips around each event — much smaller than full matches
#     downloader.downloadGames(
#         files=["Clips.zip"],
#         split=["test"],
#     )

# if __name__ == "__main__":
#     download_clips()