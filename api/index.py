from flask import Flask, request
import requests
import re

app = Flask(__name__)

def fetch_fb_count(page_id):
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&width=340&height=70&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'([\d\.,MK]+)\s?(?:位粉丝|followers|likes|人关注)', r.text)
        return match.group(1).replace(',', '') if match else "0"
    except:
        return "0"

def fetch_insta_count(username):
    # 改用专用的社交计数 API 镜像，不再爬取网页
    url = f"https://api.socialcounts.org/instagram-live-follower-count/search/{username}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        # 该接口通常返回 {"followers": 511000000, ...}
        if "followers" in data:
            return str(data["followers"])
        return "0"
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
