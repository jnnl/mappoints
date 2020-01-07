from base64 import b64encode

def check_url_get(client, body, status=200):
    """
    Check that the url contained in the _url attribute
    of the JSON object can be accessed by the GET method.

    Inspired by the check methods in section
    'Testing Flask Applications part 2' of the course material.

    Parameters:
    - client: APIClient used in the tests
    - body: response body dictionary
    - status: expected response status (default: 200)

    Returns:
    - True if the response status code matches the expected status, else False
    """

    response = client.get(body['_url'])
    return response.status_code == status

def check_parent_get(client, body, status=200):
    """
    Check that the url contained in the _parent attribute
    of the JSON object can be accessed by the GET method.

    Parameters:
    - client: APIClient used in the tests
    - body: response body dictionary
    - status: expected response status (default: 200)

    Returns:
    - True if the response status code matches the expected status, else False
    """

    response = client.get(body['_parent'])
    return response.status_code == status

def check_creator_get(client, body, status=200):
    """
    Check that the url contained under the creator attribute
    of the JSON object can be accessed by the GET method.

    Parameters:
    - client: APIClient used in the tests
    - body: response body dictionary
    - status: expected response status (default: 200)

    Returns:
    - True if the response status code matches the expected status, else False
    """

    response = client.get(body['creator']['_url'])
    return response.status_code == status

def check_point_get(client, body, status=200):
    """
    Check that the url contained under the point attribute
    of the JSON object can be accessed by the GET method.

    Parameters:
    - client: APIClient used in the tests
    - body: response body dictionary
    - status: expected response status (default: 200)

    Returns:
    - True if the response status code matches the expected status, else False
    """

    response = client.get(body['point']['_url'])
    return response.status_code == status

def get_basic_auth_header(data):
    """
    Return a HTTP Basic authentication header string from
    a string with form 'username:password'.

    Parameters:
    - data: string with the form 'username:password'

    Returns:
    - basic auth string with the username:password field base64-encoded
    """

    return 'Basic {}'.format(b64encode(str.encode(data)).decode())
