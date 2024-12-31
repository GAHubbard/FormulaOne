"""
This file contains all the support functions
Created by: Graham Hubbard
Date: 2024-12-28
"""


import urllib.parse as url


def create_url(scheme: str, netloc: str, path: str, params: str = '', query_parameters: dict = {}, fragment: str = "") -> str:
    """
    Returns encoded url with given url connection type, action and parameters
    """
    query = url.urlencode(query_parameters)
    url_tuple = (scheme, netloc, path, params, query, fragment)
    unparsed_url = url.urlunparse(url_tuple)
    return unparsed_url