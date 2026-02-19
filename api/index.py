import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 平台抓取函数 ---

def get_fb_followers(page_id):
    try:
        url = f"https://www.facebook.com/{page_id}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        # 兼容不同地区的文字，寻找 followers 前面的数字
        match = re.search(r'([\dKM\.,]+)\s?followers', r.text)
        if match:
            return match.group(1).replace(',', '')
        return "0"
    except:
        return "0"

def get_ins_followers(user_id):
    try:
        url = f"https://www.instagram.com/{user_id}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', r.text)
        return str(match.group(1)) if match else "0"
    except:
        return "0"

def get_tiktok_followers(user_id):
    try:
        url = f"https://countik.com/api/userinfo/{user_id}"
        r = requests.get(url, timeout=10)
        data = r.json()
        return str(data.get('followerCount', '0'))
    except:
        return "0"

# --- 路由配置 ---

@app.route('/')
def home():
    pt = request.args.get('type', '').lower()
    uid = request.args.get('id', '')
    
    if not pt or not uid:
        return "Usage: ?type=fb&id=xxx"

    if pt == 'fb':
        return get_fb_followers(uid)
    elif pt == 'ins':
        return get_ins_followers(uid)
    elif pt == 'tiktok':
        return get_tiktok_followers(uid)
    elif pt == 'twitch':
        # 暂时返回固定值测试
        return "123"
    
    return "0"

# ！！！ 关键：这行是给 Vercel 用的 ！！！
app = app
