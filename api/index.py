from flask import Flask, request
import requests
import re

app = Flask(__name__)

def fetch_fb_count(page_id):
    """
    之前的成功方案：抓取 Facebook Page Plugin 接口
    """
    # 模拟 iPhone 访问，诱导 FB 返回轻量级插件页面
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&width=340&height=70&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            # 兼容多种语言的粉丝数描述
            match = re.search(r'([\d\.,MK]+)\s?(?:位粉丝|followers|likes|人关注)', r.text)
            if match:
                return match.group(1).replace(',', '')
    except:
        pass
    return "0"

def fetch_tiktok_count(user_id):
    """
    TikTok 使用 Countik 第三方接口 (目前 Vercel 环境最稳)
    """
    try:
        r = requests.get(f"https://countik.com/api/userinfo/{user_id}", timeout=10)
        return str(r.json().get('followerCount', '0'))
    except:
        return "0"

@app.route('/')
def home():
    pt = request.args.get('type', '').lower()
    uid = request.args.get('id', '')
    
    if not pt or not uid:
        return "System Online. Usage: ?type=fb&id=xxx"

    if pt == 'fb':
        return fetch_fb_count(uid)
    elif pt == 'tiktok':
        return fetch_tiktok_count(uid)
    elif pt == 'twitch':
        return "888" # 依然保留这个测试点
    
    return "0"

app = app
