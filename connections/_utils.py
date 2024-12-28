"""
Description
"""


from urllib.parse import urlencode


def create_url(url: str, connection_type: str, action: str, parameters = {}) -> str:
    """
    Returns encoded url with given url connection type, action and parameters
    """
    parameters_encoded = urlencode(parameters)
    encoded_url = f'{connection_type}://{url}/{action}{"?" if parameters else ""}{parameters_encoded}'
    return encoded_url