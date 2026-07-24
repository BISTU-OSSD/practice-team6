def create_movie(title, genre, rating):
    if not title or not genre or not rating:
        return None
    return {
        "title": title,
        "genre": genre,
        "rating": rating,
    }


def add_to_watched(user_data, movie):
    user_data["watched"].append(movie)


def add_to_watchlist(user_data, movie):
    user_data["watchlist"].append(movie)


def watch_movie(user_data, title):
    target_movie = None
    for movie in user_data["watchlist"]:
        if movie["title"] == title:
            target_movie = movie
            break
    if target_movie:
        user_data["watchlist"].remove(target_movie)
        user_data["watched"].append(target_movie)
    return user_data


def get_watched_avg_rating(user_data):
    watched = user_data.get("watched", [])
    if not watched:
        return 0.0
    total_score = sum(movie["rating"] for movie in watched)
    return total_score / len(watched)


def get_most_watched_genre(user_data):
    watched = user_data.get("watched", [])
    if not watched:
        return None
    genre_count = {}
    for movie in watched:
        genre = movie["genre"]
        genre_count[genre] = genre_count.get(genre, 0) + 1
    max_genre = max(genre_count, key=genre_count.get)
    return max_genre


def get_unique_watched(user_data):
    my_watched = user_data.get("watched", [])
    if not my_watched:
        return []

    my_titles = set()
    for movie in my_watched:
        title = movie.get("title")
        if title:
            my_titles.add(title)

    friend_all_titles = set()
    for friend in user_data.get("friends", []):
        for movie in friend.get("watched", []):
            title = movie.get("title")
            if title:
                friend_all_titles.add(title)

    unique_titles = my_titles - friend_all_titles
    result = [movie for movie in my_watched if movie.get("title") in unique_titles]
    return result


def get_friends_unique_watched(user_data):
    my_titles = set()
    for movie in user_data.get("watched", []):
        title = movie.get("title")
        if title:
            my_titles.add(title)

    seen_titles = set()
    friend_movies = []

    for friend in user_data.get("friends", []):
        for movie in friend.get("watched", []):
            movie_title = movie.get("title")
            if movie_title and movie_title not in seen_titles:
                seen_titles.add(movie_title)
                friend_movies.append(movie)

    result = [movie for movie in friend_movies if movie.get("title") not in my_titles]
    return result


def get_available_recs(user_data):
    subscriptions = set(user_data.get("subscriptions", []))
    if not subscriptions:
        return []

    friend_recommendations = get_friends_unique_watched(user_data)
    result = []
    for movie in friend_recommendations:
        # 只推荐有 host 字段且匹配订阅的电影
        if "host" in movie and movie["host"] in subscriptions:
            result.append(movie)
    return result


def get_new_rec_by_genre(user_data):
    favorite_genre = get_most_watched_genre(user_data)
    if favorite_genre is None:
        return []

    friend_recommendations = get_friends_unique_watched(user_data)
    result = []
    for movie in friend_recommendations:
        if movie.get("genre") == favorite_genre:
            result.append(movie)
    return result


def get_rec_from_favorites(user_data):
    friend_watched_titles = {
        movie.get("title")
        for friend in user_data.get("friends", [])
        for movie in friend.get("watched", [])
        if movie.get("title")
    }

    seen_titles = set()
    recommendations = []
    for movie in user_data.get("favorites", []):
        movie_title = movie.get("title")
        if not movie_title:
            continue
        if movie_title in friend_watched_titles or movie_title in seen_titles:
            continue
        seen_titles.add(movie_title)
        recommendations.append(movie)

    return recommendations


def main():
    watched_scifi_one = create_movie("星际远航", "科幻", 4.8)
    watched_scifi_one.update({"id": 1, "host": "Netflix"})

    watched_scifi_two = create_movie("月球基地", "科幻", 4.6)
    watched_scifi_two.update({"id": 2, "host": "Prime Video"})

    watchlist_comedy = create_movie("周末喜剧", "喜剧", 4.2)
    watchlist_comedy.update({"id": 3, "host": "Netflix"})

    friend_netflix_scifi = create_movie("未来城市", "科幻", 4.7)
    friend_netflix_scifi.update({"id": 4, "host": "Netflix"})

    friend_disney_scifi = create_movie("银河少年", "科幻", 4.5)
    friend_disney_scifi.update({"id": 5, "host": "Disney+"})

    friend_comedy = create_movie("欢乐旅程", "喜剧", 4.3)
    friend_comedy.update({"id": 6, "host": "Netflix"})

    favorite_unique = create_movie("独家收藏", "剧情", 4.9)
    favorite_unique.update({"id": 7, "host": "Prime Video"})

    user_data = {
        "watched": [],
        "watchlist": [],
        "friends": [
            {
                "watched": [
                    watched_scifi_one,
                    friend_netflix_scifi,
                    friend_disney_scifi,
                ]
            },
            {
                "watched": [
                    friend_netflix_scifi.copy(),
                    friend_comedy,
                ]
            },
        ],
        "subscriptions": ["Netflix", "Prime Video"],
        "favorites": [
            friend_netflix_scifi,
            favorite_unique,
        ],
    }

    add_to_watched(user_data, watched_scifi_one)
    add_to_watched(user_data, watched_scifi_two)
    add_to_watchlist(user_data, watchlist_comedy)
    watch_movie(user_data, watchlist_comedy["title"])

    watched_titles = [movie["title"] for movie in user_data["watched"]]
    unique_titles = [
        movie["title"] for movie in get_unique_watched(user_data)
    ]
    friend_unique_titles = [
        movie["title"] for movie in get_friends_unique_watched(user_data)
    ]
    available_titles = [
        movie["title"] for movie in get_available_recs(user_data)
    ]
    genre_titles = [
        movie["title"] for movie in get_new_rec_by_genre(user_data)
    ]
    favorite_titles = [
        movie["title"] for movie in get_rec_from_favorites(user_data)
    ]

    print("观影派对功能演示")
    print(f"已看电影: {watched_titles}")
    print(f"已看电影平均评分: {get_watched_avg_rating(user_data):.2f}")
    print(f"最常观看类型: {get_most_watched_genre(user_data)}")
    print(f"仅自己看过: {unique_titles}")
    print(f"仅好友看过: {friend_unique_titles}")
    print(f"订阅平台可观看推荐: {available_titles}")
    print(f"最常观看类型推荐: {genre_titles}")
    print(f"收藏夹推荐: {favorite_titles}")


if __name__ == "__main__":
    main()
