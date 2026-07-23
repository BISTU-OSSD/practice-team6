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
    my_watched = user_data["watched"]
    my_ids = {movie["id"] for movie in my_watched}

    friend_all_ids = set()
    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            friend_all_ids.add(movie["id"])

    unique_ids = my_ids - friend_all_ids
    result = [movie for movie in my_watched if movie["id"] in unique_ids]
    return result


def get_friends_unique_watched(user_data):
    my_ids = {movie["id"] for movie in user_data["watched"]}
    seen_ids = set()
    friend_movies = []

    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            movie_id = movie["id"]
            if movie_id not in seen_ids:
                seen_ids.add(movie_id)
                friend_movies.append(movie)

    result = [movie for movie in friend_movies if movie["id"] not in my_ids]
    return result


def get_available_recs(user_data):
    subscriptions = set(user_data.get("subscriptions", []))
    if not subscriptions:
        return []

    friend_recommendations = get_friends_unique_watched(user_data)
    return [
        movie
        for movie in friend_recommendations
        if movie.get("host") in subscriptions
    ]


def get_new_rec_by_genre(user_data):
    favorite_genre = get_most_watched_genre(user_data)
    if favorite_genre is None:
        return []

    friend_recommendations = get_friends_unique_watched(user_data)
    return [
        movie
        for movie in friend_recommendations
        if movie.get("genre") == favorite_genre
    ]


def get_rec_from_favorites(user_data):
    friend_watched_ids = {
        movie["id"]
        for friend in user_data.get("friends", [])
        for movie in friend.get("watched", [])
    }

    seen_ids = set()
    recommendations = []
    for movie in user_data.get("favorites", []):
        movie_id = movie["id"]
        if movie_id in friend_watched_ids or movie_id in seen_ids:
            continue
        seen_ids.add(movie_id)
        recommendations.append(movie)

    return recommendations
