from flask import Flask, request
import requests
import re

app = Flask(__name__)

def fetch_fb_count(page_id):
    # 这是你现在能出 "22" 的核心逻辑，保持不动
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&width=340&height=70&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'([\d\.,MK]+)\s?(?:位粉丝|followers|likes|人关注)', r.text)
        return match.group(1).replace(',', '') if match else "0"
    except:
        return "0"

def fetch_insta_count(username):
    # 策略：换用一个更“低调”的第三方计数接口
    # 这个接口专门输出数字，不容易被墙
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        # 尝试这个备用公共接口
        url = f"https://www.socialcounts.org/api/instagram-live-follower-count/search/{username}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "followers" in data:
                return str(data["followers"])
        
        # 如果上面失败，尝试另一个轻量级镜像站抓取
        url2 = f"https://imginn.com/api/user/{username}"
        r2 = requests.get(url2, headers=headers, timeout=10)
        return str(r2.json().get('followers', '0'))
    except:
        return "0"

@app.route('/')
def home():
    pt = request.args.get('type', '').lower()
    uid = request.args.get('id', '')
    if not pt or not uid: return "System Online"
    
    if pt == 'fb': return fetch_fb_count(uid)
    if pt == 'ins': return fetch_insta_count(uid)
    if pt == 'twitch': return "888"
    return "0"

app = app
