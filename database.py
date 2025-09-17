from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client["movie_bot"]

users_col = db["users"]
videos_col = db["videos"]
episodes_col = db["episodes"]
verify_col = db["verify_links"]
ads_col = db["ads"]
logs_col = db["logs"]

def save_user(user_id, username=None):
    users_col.update_one({"user_id": user_id}, {"$set": {"username": username}}, upsert=True)

def save_video(file_id, series_name, season, episode_name):
    videos_col.update_one(
        {"file_id": file_id},
        {"$set": {"series": series_name, "season": season, "episode": episode_name, "added": datetime.datetime.now()}},
        upsert=True
    )

def get_video(series_name, season, episode_name):
    return videos_col.find_one({"series": series_name, "season": season, "episode": episode_name})

def save_episode(series_name, season, episode_name, file_id=None):
    episodes_col.update_one(
        {"series": series_name, "season": season, "episode": episode_name},
        {"$set": {"file_id": file_id}},
        upsert=True
    )

def get_seasons(series_name):
    return sorted(episodes_col.distinct("season", {"series": series_name}))

def get_episodes(series_name, season):
    return list(episodes_col.find({"series": series_name, "season": season}))

def save_verify_link(user_id, link):
    verify_col.update_one(
        {"user_id": user_id, "link": link},
        {"$set": {"verified": False, "created": datetime.datetime.now()}},
        upsert=True
    )

def verify_link(user_id, link):
    result = verify_col.find_one({"user_id": user_id, "link": link})
    if result:
        verify_col.update_one({"_id": result["_id"]}, {"$set": {"verified": True}})
        return True
    return False

def track_ad_click(link, user_id):
    ads_col.update_one({"link": link}, {"$push": {"clicks": user_id}}, upsert=True)

def log_action(action, user_id=None, details=None):
    logs_col.insert_one({"action": action, "user_id": user_id, "details": details, "time": datetime.datetime.now()})
