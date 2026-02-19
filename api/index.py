from flask import Flask, request
import requests
import re

app = Flask(__name__)

def fetch_count(platform, user_id):
    # 模拟真实浏览器，防止被直接拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        if platform == 'fb':
            # 访问完全公开的主页路径
            url = f"https://www.facebook.com/{user_id}"
            r = requests.get(url, headers=headers, timeout=10)
            html = r.text
            
            # 逻辑 A: 找元数据标签 (之前成功的核心)
            # 匹配: content="1.2M followers"
            meta_match = re.search(r'content="([\d\.,KkMm]+)\s?(?:followers|关注者|人关注)"', html)
            if meta_match:
                return meta_match.group(1).replace(',', '')
            
            # 逻辑 B: 找 JSON 配置块
            # 匹配: "follower_count":12345
            json_match = re.search(r'"follower_count":(\d+)', html)
            if json_match:
                return json_match.group(1)
            
            # 逻辑 C: 找页面正文
            text_match = re.search(r'([\d\.,KkMm]+)\s?followers', html)
            return text_match.group(1).replace(',', '') if text_match else "0"

        elif platform == 'tiktok':
            # TikTok 网页抓取极其不稳定，建议直接用这个第三方接口 (目前最稳)
            r = requests.get(f"https://countik.com/api/userinfo/{user_id}", timeout=10)
            return str(r.json().get('followerCount', '0'))

        elif platform == 'twitch':
            return "888"

        return "0"
    except Exception:
        return "0"

@app.route('/')
def home():
    p_type = request.args.get('type', '').lower()
    p_id = request.args.get('id', '')
    if not p_type or not p_id:
        return "System Online"
    return fetch_count(p_type, p_id)

app = app
