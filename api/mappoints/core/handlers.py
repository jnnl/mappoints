from mappoints.core.serializers import UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    """
    Return the User's details along with the JWT token on JWT login.

    Adapted from https://getblimp.github.io/django-rest-framework-jwt/
    under JWT_RESPONSE_PAYLOAD_HANDLER.

    Parameters:
        - token: the JWT token to return
        - user: the user resource to serialize
        - request: the request context applied to the serializer

    Returns:
        - a dictionary containing the JWT token and user details
    """

    context = {'request': request}
    user_representation = UserSerializer(user, context=context)

    return {
        'token': token,
        'user': user_representation.data
    }

