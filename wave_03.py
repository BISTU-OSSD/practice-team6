def get_unique_watched(user_data):
    my_watched = user_data["watched"]
    my_ids = {movie["id"] for movie in my_watched}

    friend_all_ids = set()
    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            friend_all_ids.add(movie["id"])

    unique_ids = my_ids - friend_all_ids
    result = [m for m in my_watched if m["id"] in unique_ids]
    return result


def get_friends_unique_watched(user_data):
    my_ids = {movie["id"] for movie in user_data["watched"]}
    seen_id = set()
    friend_movies = []

    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            mid = movie["id"]
            if mid not in seen_id:
                seen_id.add(mid)
                friend_movies.append(movie)

    result = [m for m in friend_movies if m["id"] not in my_ids]
    return result