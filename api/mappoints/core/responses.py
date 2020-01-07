from rest_framework.response import Response
from mappoints.core.utils import get_url, get_parent_url

class LinkedCollectionResponse(Response):
    """
    A specialized subclass of Response that appends '_url' and '_parent'
    link attributes and wraps the list of resources under the '_items' attribute.

    Used when a list of items is requested from a collection (e.g. /users/)
    """

    def __init__(self, data, request, *args, **kwargs):
        uri = request.build_absolute_uri()
        super().__init__({
            '_items': data,
            '_url': get_url(uri),
            '_parent': get_parent_url(uri)
        }, *args, **kwargs)

class LinkedInstanceResponse(Response):
    """
    A specialized subclass of Response that appends a '_parent' link attribute
    to the response containing the resource representation.

    Used when a single resource instance is requested (e.g. /users/1/)
    """

    def __init__(self, data, request, *args, **kwargs):
        uri = request.build_absolute_uri()
        if data.get('_url'):
            parent_url = get_parent_url(data['_url'])
        else:
            parent_url = get_parent_url(uri)

        super().__init__({
            **data,
            '_parent': parent_url
        }, *args, **kwargs)
