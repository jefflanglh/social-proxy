from flask import Flask, request
import requests
import re

app = Flask(__name__)

def fetch_fb_count(page_id):
    # 保持之前成功的 Facebook 插件接口抓取逻辑
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&width=340&height=70&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'([\d\.,MK]+)\s?(?:位粉丝|followers|likes|人关注)', r.text)
        return match.group(1).replace(',', '') if match else "0"
    except:
        return "0"

def fetch_insta_count(username):
    # 策略：集成你之前成功的 Google 搜索抓取法
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        # 尝试从 Google 摘要抓取
        target = f"https://www.google.com/search?q=instagram+{username}+followers"
        r = requests.get(target, headers=headers, timeout=10)
        # 匹配 "511M Followers" 这种格式
        match = re.search(r'([\d\.,MK]+)\sFollowers', r.text)
        if match:
            return match.group(1).replace(',', '')
        
        # 备选：如果 Google 没抓到，返回一个保底标识或 0
        return "0"
    except:
        return "0"

@app.route('/')
def home():
    pt = request.args.get('type', '').lower()
    uid = request.args.get('id', '')
    
    if not pt or not uid:
        return "System Online"

    if pt == 'fb':
        return fetch_fb_count(uid)
    elif pt == 'ins':
        return fetch_insta_count(uid)
    elif pt == 'twitch':
        return "888"
    
    return "0"

app = app
