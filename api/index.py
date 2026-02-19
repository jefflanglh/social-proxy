from flask import Flask, request
import requests
import re

app = Flask(__name__)

# 配置你的 Twitch 密钥（建议稍后在 Vercel 环境变量里设置更安全）
TWITCH_ID = "你的_CLIENT_ID" 
TWITCH_SECRET = "你的_CLIENT_SECRET"

def get_twitch_followers(username):
    try:
        # 获取 Token
        auth_res = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={TWITCH_ID}&client_secret={TWITCH_SECRET}&grant_type=client_credentials")
        token = auth_res.json()['access_token']
        # 获取用户 ID
        u_res = requests.get(f"https://api.twitch.tv/helix/users?login={username}", headers={"Client-ID": TWITCH_ID, "Authorization": f"Bearer {token}"})
        uid = u_res.json()['data'][0]['id']
        # 获取粉丝数
        f_res = requests.get(f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={uid}", headers={"Client-ID": TWITCH_ID, "Authorization": f"Bearer {token}"})
        return str(f_res.json()['total'])
    except:
        return "0"

def get_fb_followers(page_id):
    try:
        url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}"
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0) AppleWebKit/605.1.15'}
        r = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'([\d\.,MK]+)\s?(位粉丝|followers)', r.text)
        return match.group(1).replace(',', '') if match else "0"
    except:
        return "0"

@app.route('/')
def home():
    platform = request.args.get('type')
    user_id = request.args.get('id')
    if platform == 'twitch' and user_id:
        return get_twitch_followers(user_id)
    elif platform == 'fb' and user_id:
        return get_fb_followers(user_id)
    return "Usage: /?type=fb&id=PAGE_ID"
