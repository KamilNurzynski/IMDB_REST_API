from rest_framework.throttling import UserRateThrottle

"""
In this file are custom throttling classes.
"""


class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'  # tutaj piszemy nazwę, której użyjemy w settings.


class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
