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
        g = movie["genre"]
        genre_count[g] = genre_count.get(g, 0) + 1
    max_genre = max(genre_count, key=genre_count.get)
    return max_genre