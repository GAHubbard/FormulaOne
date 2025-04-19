"""
This file contains all the support functions
Created by: Graham Hubbard
Date: 2024-12-28
"""


import urllib.parse as url


def create_url(scheme: str, netloc: str, path: str, params: str = '', query_parameters: dict = {}, fragment: str = "") -> str:
    """
    Returns encoded url with given url connection type, action and parameters
    !!** THERE IS A CHANCE THAT REQUESTS HANDLES THIS ALREADY SO NO NEED TO DO IT WITH THE F1 API**!!
    """
    query = url.urlencode(query_parameters)                     # encode only the parameter section of the url
    url_tuple = (scheme, netloc, path, params, query, fragment) # create a tuple of all the components
    unparsed_url = url.urlunparse(url_tuple)                    # create the full url
    return unparsed_url  # return url