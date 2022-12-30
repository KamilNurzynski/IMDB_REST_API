from rest_framework.throttling import UserRateThrottle

"""
In this file are custom throttling classes.
"""


class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'


class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
