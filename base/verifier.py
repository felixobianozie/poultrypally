"""
Custom functions, decorators & decoratory callback functions for verifications.
They usually would return a boolean type.
"""

from django.contrib import messages
from crequest.middleware import CrequestMiddleware


def user_not_logged_in(user):
    """Returns True if user is not logged in"""

    # Fetch current request instance
    request = CrequestMiddleware.get_request()

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged into the system!")
        return False
    return True

def user_owns_resource(request, resource):
    """Returs True if user owns given resource"""
    if resource.created_by:
        return request.user == resource.created_by
    return False
