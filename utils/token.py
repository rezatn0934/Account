import random
import string
import jwt

from config.config import settings
from schemas.token import AccessToken, RefreshToken


def create_access_token(payload: AccessToken):

    """
    The create_access_token function takes a payload and returns an encoded JWT.
    The payload is the AccessToken object, which contains the user's id, username, email address and role.
    The encoded JWT is returned to be used as an access token.

    :param payload: AccessToken: Pass in the accesstoken object
    :return: A string that is the encoded jwt
    :doc-author: Trelent
    """
    payload = payload.model_dump()
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(payload: RefreshToken):

    """
    The create_refresh_token function takes a RefreshToken object as an argument and returns the encoded JWT.
    The payload is dumped into a dictionary using the model_dump method, which we created in our models file.
    We then encode this payload with our secret key and algorithm.

    :param payload: RefreshToken: Pass in the payload for the jwt
    :return: A string
    :doc-author: Trelent
    """
    payload = payload.model_dump()
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str):

    """
    The decode_token function takes a token as an argument and returns the payload.
    The decode_token function uses the jwt library to decode the token using our SECRET_KEY and ALGORITHM.

    :param token: str: Pass in the token that is being decoded
    :return: A dictionary with the token payload
    :doc-author: Trelent
    """
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload


def get_random_string(length):

    """
    The get_random_string function takes a length argument and returns a random string of that length.
    The function uses the string module's ascii_lowercase constant to generate the random strings.

    :param length: Specify the length of the string that will be returned
    :return: A string of random letters of the specified length
    :doc-author: Trelent
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
