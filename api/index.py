from flask import Flask, request
import requests
import re

app = Flask(__name__)

def get_fb_followers(page_id):
    try:
        url = f"https://www.facebook.com/{page_id}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        # 匹配 FB 粉丝数的正则
        match = re.search(r'(\d?[kKmM\d\.,]+)\s?followers', r.text)
        if match:
            # 去掉逗号，只保留数字和单位
            val = match.group(1).replace(',', '')
            return val
        return "0"
    except Exception as e:
        return "0"

def get_ins_followers(user_id):
    try:
        url = f"https://www.instagram.com/{user_id}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        # 改进后的正则
        match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', r.text)
        return str(match.group(1)) if match else "0"
    except:
        return "0"

def get_tiktok_followers(user_id):
    try:
        # 使用第三方免费接口，因为 TikTok 官网非常难爬
        url = f"https://countik.com/api/userinfo/{user_id}"
        r = requests.get(url, timeout=10)
        return str(r.json().get('followerCount', '0'))
    except:
        return "0"

def get_twitch_followers(user_id):
    try:
        # 注意：Twitch 官方通常需要 API Key，这里是一个简化的逻辑
        return "0"
    except:
        return "0"

@app.route('/')
def home():
    platform = request.args.get('type')
    user_id = request.args.get('id')
    
    if not platform or not user_id:
        return "Usage: /?type=fb&id=PAGE_ID"

    if platform == 'fb': return get_fb_followers(user_id)
    if platform == 'ins': return get_ins_followers(user_id)
    if platform == 'tiktok': return get_tiktok_followers(user_id)
    if platform == 'twitch': return get_twitch_followers(user_id)
    
    return "0"

# 必须有这行供 Vercel 调用
app = app
