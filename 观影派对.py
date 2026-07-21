def create_movie(title, genre, rating):
    if not title or not genre or not rating:
        return None
    return {
        "title": title,
        "genre": genre,
        "rating": rating
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