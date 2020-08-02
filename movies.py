import time


class MovieList():
    def __init__(self, movies = []):
        """
        [
            {
                "title": "The Princess Bride", "added": 1595908648
            },
            {
                "title": "Fargo", "added": 1595908648
            }
        ]
        """
        self.movies = movies

    def getMovieID(self, title: str) -> int:
        for pos, t in enumerate(self.movies):
            if title.lower() == t["title"].lower():
                return pos
        return None

    def add(self, title: str) -> bool:
        for movie in self.movies:
            if movie['title'].lower() == title.lower():
                # Movie is already in the list
                return False

        this_movie = {
            "title": title,
            "added": time.time()
        }

        self.movies.append(this_movie)
        return True

    def remove(self, indexes: list) -> bool:
        # Even if there is only one item to remove, we expect a list with just
        # the one movie number in it
        for idx in sorted(indexes, reverse=True):
            del self.movies[idx]
        return True

