import math


def get_stars_from_rating(rating):
    """
    Returns the number of full stars, empty stars and whether it has a half star
    """
    full_stars = math.floor(rating)
    empty_stars = math.floor(5 - rating)
    half_star = (full_stars + empty_stars) < 5
    return full_stars, empty_stars, half_star

