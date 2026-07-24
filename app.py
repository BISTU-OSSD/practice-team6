from flask import Flask, render_template, request, jsonify
from party import (
    create_movie,
    add_to_watched,
    add_to_watchlist,
    watch_movie,
    get_watched_avg_rating,
    get_most_watched_genre,
    get_unique_watched,
    get_friends_unique_watched,
    get_available_recs,
    get_new_rec_by_genre,
    get_rec_from_favorites
)

app = Flask(__name__)

# 模拟用户数据（实际项目中可用数据库存储）
# 这里用字典存储每个用户的观影数据，方便多人使用
users = {}


def get_or_create_user(username):
    """获取或创建用户数据"""
    if username not in users:
        users[username] = {
            "watched": [],
            "watchlist": [],
            "friends": [],
            "subscriptions": [],
            "favorites": []   # ← 新增这一行
        }
    return users[username]

# ============================================
# 页面路由
# ============================================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


# ============================================
# API 路由 - 用户管理
# ============================================

@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    """获取用户数据"""
    user = get_or_create_user(username)
    return jsonify({
        "username": username,
        "watched": user["watched"],
        "watchlist": user["watchlist"],
        "friends": user["friends"],
        "subscriptions": user["subscriptions"]
    })


# ============================================
# API 路由 - Wave 1: 基础数据操作
# ============================================

@app.route('/api/movie', methods=['POST'])
def api_create_movie():
    """创建电影"""
    import time
    import random
    
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    rating = data.get('rating')

    movie = create_movie(title, genre, rating)
    if movie is None:
        return jsonify({"error": "参数无效，请检查 title、genre、rating"}), 400
    
    # 自动生成唯一 ID
    movie["id"] = int(time.time() * 1000) + random.randint(1, 1000)
    
    return jsonify(movie)


@app.route('/api/user/<username>/watched', methods=['POST'])
def api_add_to_watched(username):
    """添加电影到已看列表"""
    user = get_or_create_user(username)
    data = request.get_json()
    movie = data.get('movie')

    if not movie or 'title' not in movie:
        return jsonify({"error": "电影数据无效"}), 400

    add_to_watched(user, movie)
    return jsonify({"message": f"已添加 {movie['title']} 到已看列表", "watched": user["watched"]})


@app.route('/api/user/<username>/watchlist', methods=['POST'])
def api_add_to_watchlist(username):
    """添加电影到想看列表"""
    user = get_or_create_user(username)
    data = request.get_json()
    movie = data.get('movie')

    if not movie or 'title' not in movie:
        return jsonify({"error": "电影数据无效"}), 400

    add_to_watchlist(user, movie)
    return jsonify({"message": f"已添加 {movie['title']} 到想看列表", "watchlist": user["watchlist"]})


@app.route('/api/user/<username>/watch', methods=['POST'])
def api_watch_movie(username):
    """将电影从想看移到已看"""
    user = get_or_create_user(username)
    data = request.get_json()
    title = data.get('title')

    result = watch_movie(user, title)
    if result:
        return jsonify({"message": f"已观看 {title}", "watched": user["watched"], "watchlist": user["watchlist"]})
    else:
        return jsonify({"error": f"未找到电影 {title}"}), 404


# ============================================
# API 路由 - Wave 2: 数据统计
# ============================================

@app.route('/api/user/<username>/avg-rating', methods=['GET'])
def api_get_watched_avg_rating(username):
    """获取已看平均评分"""
    user = get_or_create_user(username)
    avg = get_watched_avg_rating(user)
    return jsonify({"username": username, "avg_rating": avg})


@app.route('/api/user/<username>/most-genre', methods=['GET'])
def api_get_most_watched_genre(username):
    """获取看最多的类型"""
    user = get_or_create_user(username)
    genre = get_most_watched_genre(user)
    return jsonify({"username": username, "most_watched_genre": genre})


# ============================================
# API 路由 - Wave 3: 个人与好友对比
# ============================================

@app.route('/api/user/<username>/friends', methods=['POST'])
def api_add_friend(username):
    """添加好友"""
    user = get_or_create_user(username)
    data = request.get_json()
    friend_username = data.get('friend')

    if not friend_username:
        return jsonify({"error": "好友用户名不能为空"}), 400

    # 创建好友的数据结构（如果不存在）
    friend_data = get_or_create_user(friend_username)

    # 检查是否已经是好友
    for friend in user["friends"]:
        if friend.get("username") == friend_username:
            return jsonify({"error": f"{friend_username} 已经是好友"}), 400

    # 添加到好友列表（简化版本，只存用户名，实际需要好友的完整数据）
    user["friends"].append(
        {"username": friend_username, "watched": friend_data["watched"], "watchlist": friend_data["watchlist"]})

    return jsonify({"message": f"已添加好友 {friend_username}", "friends": user["friends"]})


@app.route('/api/user/<username>/unique-watched', methods=['GET'])
def api_get_unique_watched(username):
    """获取用户独看电影"""
    user = get_or_create_user(username)
    unique = get_unique_watched(user)
    return jsonify({"username": username, "unique_watched": unique})


@app.route('/api/user/<username>/friends-unique-watched', methods=['GET'])
def api_get_friends_unique_watched(username):
    """获取好友独看电影"""
    user = get_or_create_user(username)
    unique = get_friends_unique_watched(user)
    return jsonify({"username": username, "friends_unique_watched": unique})


# ============================================
# API 路由 - Wave 4 & 5: 推荐系统
# ============================================

@app.route('/api/user/<username>/subscriptions', methods=['POST'])
def api_add_subscription(username):
    """添加订阅服务"""
    user = get_or_create_user(username)
    data = request.get_json()
    service = data.get('service')

    if not service:
        return jsonify({"error": "订阅服务不能为空"}), 400

    if service not in user["subscriptions"]:
        user["subscriptions"].append(service)

    return jsonify({"message": f"已添加订阅 {service}", "subscriptions": user["subscriptions"]})


@app.route('/api/user/<username>/available-recs', methods=['GET'])
def api_get_available_recs(username):
    """获取基于订阅的推荐"""
    user = get_or_create_user(username)
    recs = get_available_recs(user)
    return jsonify({"username": username, "available_recs": recs})


@app.route('/api/user/<username>/rec-by-genre', methods=['GET'])
def api_get_new_rec_by_genre(username):
    """获取基于类型的推荐"""
    user = get_or_create_user(username)
    recs = get_new_rec_by_genre(user)
    return jsonify({"username": username, "rec_by_genre": recs})


@app.route('/api/user/<username>/rec-from-favorites', methods=['GET'])
def api_get_rec_from_favorites(username):
    """获取基于收藏的推荐"""
    user = get_or_create_user(username)
    recs = get_rec_from_favorites(user)
    return jsonify({"username": username, "rec_from_favorites": recs})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)