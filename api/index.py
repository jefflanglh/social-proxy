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
            return None # 失败返回 None，方便后面判定
        return res_data.get("access_token")
    except:
        return None

def fetch_twitch_count(username):
    token = get_twitch_token()
    if not token: 
        return "Error_Token_Auth_Failed" # 这里会直接显示在网页上，告诉你 Token 没拿到
    
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    try:
        # 1. 获取 User ID
        user_url = f"https://api.twitch.tv/helix/users?login={username}"
        u_res = requests.get(user_url, headers=headers, timeout=5).json()
        
        if not u_res.get("data") or len(u_res["data"]) == 0:
            return "Error_User_Not_Found"
        
        user_id = u_res["data"][0]["id"]
        
        # 2. 获取粉丝总数
        fol_url = f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}"
        f_res = requests.get(fol_url, headers=headers, timeout=5).json()
        
        # 调试重点：如果接口报错（比如权限问题），返回报错信息
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

@app.route('/')
def home():
    pt = request.args.get('type', '').lower()
    uid = request.args.get('id', '')
    if not pt or not uid: return "System Online"
    
    if pt == 'fb': return fetch_fb_count(uid)
    if pt == 'twitch': return fetch_twitch_count(uid)
    return "0"

app = app
