def get_ins_followers(user_id):
    try:
        # 使用第三方镜像接口或直接抓取格式化页
        url = f"https://www.instagram.com/{user_id}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        # 匹配元数据中的粉丝数
        match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', r.text)
        return str(match.group(1)) if match else "0"
    except:
        return "0"

def get_tiktok_followers(user_id):
    try:
        # TikTok 建议使用 countik 等公共接口的中转
        url = f"https://countik.com/api/userinfo/{user_id}"
        r = requests.get(url, timeout=10)
        return str(r.json()['followerCount'])
    except:
        return "0"

# 在 home() 路由里增加判断
@app.route('/')
def home():
    platform = request.args.get('type')
    user_id = request.args.get('id')
    if platform == 'twitch': return get_twitch_followers(user_id)
    if platform == 'fb': return get_fb_followers(user_id)
    if platform == 'ins': return get_ins_followers(user_id)
    if platform == 'tiktok': return get_tiktok_followers(user_id)
    return "Usage: /?type=fb&id=PAGE_ID"
