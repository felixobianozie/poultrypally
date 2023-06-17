from django.utils.deprecation import MiddlewareMixin

# Prevent browswer caching
class NoIfModifiedSinceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.META.pop('HTTP_IF_MODIFIED_SINCE', None)