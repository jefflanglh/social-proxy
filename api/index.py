import os
from flask import Flask, request
import requests
import re

app = Flask(__name__)

# --- 环境变量读取 ---
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    try:
        r = requests.post(url, params=params, timeout=5)
        res_data = r.json()
        if r.status_code != 200:
            return None 
        return res_data.get("access_token")
    except:
        return None

def fetch_twitch_count(username):
    token = get_twitch_token()
    if not token: 
        return "Error_Token_Auth_Failed" 
    
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    try:
        user_url = f"https://api.twitch.tv/helix/users?login={username}"
        u_res = requests.get(user_url, headers=headers, timeout=5).json()
        
        if not u_res.get("data") or len(u_res["data"]) == 0:
            return "Error_User_Not_Found"
        
        user_id = u_res["data"][0]["id"]
        
        fol_url = f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}"
        f_res = requests.get(fol_url, headers=headers, timeout=5).json()
        
        if "total" in f_res:
            return str(f_res["total"])
        elif "message" in f_res:
            return f"Error_Twitch_API_{f_res['message'][:15]}"
        return "0"
    except Exception as e:
        return f"Error_Runtime_{str(e)[:15]}"

def fetch_fb_count(page_id):
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&width=340&height=70&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'([\d\.,MK]+)\s?(?:位粉丝|followers|likes|人关注)', r.text)
        return match.group(1).replace(',', '') if match else "0"
    except:
        return "0"

def fetch_tiktok_count(sec_id):
    url = f"https://countik.com/api/userinfo?sec_user_id={sec_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://countik.com/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data.get("status") == "success":
            return str(data.get("followerCount", "0"))
        return "0"
    except:
        return "0"

# --- 新增 Instagram 实时获取逻辑 ---
def fetch_insta_count(username):
    # 使用针对第三方工具优化的 API 镜像接口
    url = f"https://www.socialcounts.org/api/instagram-live-follower-count/search/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.socialcounts.org/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=8)
        data = r.json()
        # 接口返回的是一个搜索列表，通常第一个就是我们要的精准匹配
        if "items" in data and len(data["items"]) > 0:
            return str(data["items"][0]["followerCount"])
        return "0"
    except:
        return "Wait"

@app.route('/')
def home():
    pt = request.args.get('type', '').lower()
    uid = request.args.get('id', '')
    if not pt or not uid: return "System Online"
    
    if pt == 'fb': return fetch_fb_count(uid)
    if pt == 'twitch': return fetch_twitch_count(uid)
    if pt == 'tiktok': return fetch_tiktok_count(uid)
    if pt == 'ins': return fetch_insta_count(uid) # 这里的 uid 传入博主名字即可
    return "0"

app = app
