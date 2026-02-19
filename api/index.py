from flask import Flask, request
import requests
import re

app = Flask(__name__)

# --- 获取粉丝数的底层逻辑 ---
def fetch_count(platform, user_id):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        if platform == 'fb':
            # 抓取 Facebook 移动版，匹配更稳
            r = requests.get(f"https://m.facebook.com/{user_id}", headers=headers, timeout=10)
            match = re.search(r'([\d\.,KkMm]+)\s?(?:followers|人关注)', r.text)
            return match.group(1).replace(',', '') if match else "0"

        elif platform == 'ins':
            # 抓取 Instagram 网页元数据
            r = requests.get(f"https://www.instagram.com/{user_id}/", headers=headers, timeout=10)
            match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', r.text)
            return match.group(1) if match else "0"

        elif platform == 'tiktok':
            # 使用公共接口（比爬虫稳）
            r = requests.get(f"https://countik.com/api/userinfo/{user_id}", timeout=10)
            return str(r.json().get('followerCount', '0'))

        elif platform == 'twitch':
            return "888" # 测试用，如果能看到888说明系统全线通车

        return "0"
    except Exception:
        return "0"

# --- 路由入口 ---
@app.route('/')
def home():
    p_type = request.args.get('type', '').lower()
    p_id = request.args.get('id', '')
    
    if not p_type or not p_id:
        return "Usage: ?type=fb&id=xxx"
        
    return fetch_count(p_type, p_id)

# 必须声明给 Vercel 调用
app = app
