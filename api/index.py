import os
from flask import Flask, request
import requests
import re

app = Flask(__name__)

# --- 从 Vercel 环境变量中读取密钥 ---
# 确保你在后台添加的名字完全对应：TWITCH_CLIENT_ID 和 TWITCH_CLIENT_SECRET
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

def get_twitch_token():
    """使用环境变量获取 Twitch Access Token"""
    if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
        print("Error: Twitch keys not found in environment variables")
        return None
        
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    try:
        r = requests.post(url, params=params, timeout=5)
        return r.json().get("access_token")
    except Exception as e:
        print(f"Token Error: {e}")
        return None

def fetch_twitch_count(username):
    """通过官方 API 获取实时粉丝数"""
    token = get_twitch_token()
    if not token: return "Error_Token"
    
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    try:
        # 1. 获取 User ID
        user_url = f"https://api.twitch.tv/helix/users?login={username}"
        u_res = requests.get(user_url, headers=headers, timeout=5).json()
        if not u_res.get("data"): return "0"
        
        user_id = u_res["data"][0]["id"]
        
        # 2. 获取粉丝总数 (Twitch 最新 API 路径)
        fol_url = f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}"
        f_res = requests.get(fol_url, headers=headers, timeout=5).json()
        return str(f_res.get("total", "0"))
    except Exception as e:
        print(f"API Error: {e}")
        return "0"

def fetch_fb_count(page_id):
    # 保持你之前稳定的 Facebook 插件爬取逻辑
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
    
    if pt == 'fb': 
        return fetch_fb_count(uid)
    if pt == 'twitch': 
        return fetch_twitch_count(uid)
    if pt == 'ins':
        # Instagram 还是建议走你的 GitHub Action 获取那个 txt 结果
        return "Use GitHub Raw URL for Ins"
        
    return "0"

# Vercel 需要
app = app
