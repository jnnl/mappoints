from furl import furl

def get_url(input_url):
    """
    Get url without query params and fragment identifiers.

    Parameters:
        - input_url: the url string to strip from query parameters and fragments.

    Returns:
        - url string without query parameters and fragments.
    """
    url = furl(input_url)
    cleaned_url = url.remove(args=True, fragment=True)
    if cleaned_url:
        return cleaned_url.url
    else:
        return url

def get_parent_url(input_url):
    """
    Get parent url without query params and fragment identifiers.

    Parameters:
        - input_url: the url string to strip from query parameters and fragments.

    Returns:
        - url string without query parameters and fragments.
    """
    url = furl(input_url)
    cleaned_url = url.remove(args=True, fragment=True)
    cleaned_url.path.segments = cleaned_url.path.segments[:-2] + ['']
    if cleaned_url:
        return cleaned_url.url
    else:
        return url

def wrap_url(base_field):
    """
    Wrap unexpanded hyperlinked resource fields inside '_url' attribute.

    Parameters:
        - base_field: resource field whose serialized representation is wrapped
                      inside the '_url' attribute

    Returns:
        - resource field with the deserialized representation
          wrapped inside a '_url' attribute.
    """
    class CustomField(base_field):
        def to_representation(self, instance):
            rep = super().to_representation(instance)
            return {'_url': rep}

    return CustomField
