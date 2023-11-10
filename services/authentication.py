from typing import Any
import jwt

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.token import decode_token
from db.redis_db import get_redis_auth_client

redis_auth = get_redis_auth_client()


async def get_payload_from_access_token(token):
    """
    The get_payload_from_access_token function takes in a token and returns the payload of that token.
        If the access_token is expired, it raises an HTTPException with status code 401 (Unauthorized).
        If there is an invalid signature error, it raises an HTTPException with status code 400 (Bad Request).
        Otherwise, if there are any other errors raised by decode_token(), then it also raises an
            HTTPException with status code 400 (Bad Request).

    :param token: Get the payload from the access token
    :return: The payload of the access token
    :doc-author: Trelent
    """
    try:
        access_token = token.split(' ')[1]
        payload = decode_token(access_token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired access token")
    except jwt.InvalidSignatureError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access token")


async def get_payload_from_refresh_token(token):
    """
    The get_payload_from_refresh_token function takes a refresh token as an argument and returns the payload of that token.
        If the refresh token is expired, it raises an HTTPException with status code 400 and detail &quot;Expired refresh token&quot;.
        If there is any other error, it raises an HTTPException with status code 400 and detail str(e).

    :param token: Decode the token
    :return: A payload from a refresh token
    :doc-author: Trelent
    """
    try:
        payload = decode_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expired refresh token")
    except jwt.InvalidSignatureError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def validate_token(payload: dict) -> Any:
    """
    The validate_token function is a callback function that will be called by FastAPI to validate the token.
    It takes in the payload of the JWT and returns an object if it's valid, or raises an exception if it's not.

    :param payload: dict: Get the jti and user_id from the token
    :return: The user_id and jti
    :doc-author: Trelent
    """
    jti = payload.get('jti')
    user_id = payload.get('user_id')
    result = await redis_auth.get(f"user_{user_id} || {jti}")
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid token, please login again.')


class JWTAuthentication(HTTPBearer):
    authentication_header_prefix = 'Token'
    authentication_header_name = 'Authorization'

    def authenticate_header(self, request: Request):
        """
        The authenticate_header function is used to return the header value that will be used in the response.
        This function is called when a request fails with an authentication challenge, and it must return a string
        that will be set as the WWW-Authenticate header in the response.

        :param self: Represent the instance of the class
        :param request: Request: Get the request object
        :return: The authentication header prefix
        :doc-author: Trelent
        """
        return self.authentication_header_prefix

    def __init__(self, auto_error: bool = True):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and it's where you can set default values for attributes.


        :param self: Represent the instance of the class
        :param auto_error: bool: Determine whether or not to raise an exception when the authentication fails
        :return: The super class of jwtauthentication, which is the authenticator class
        :doc-author: Trelent
        """
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        """
        The __call__ function is the main function of this class. It takes in a request object and returns a payload if
        the token is valid, or None if it isn't. The __call__ function first gets the authorization header from the request
        object using get_authorization_header(). If there's no authorization header, then we return None because there's no
        token to validate. Next, we check that our prefix matches what was sent in the Authorization header using check_prefix().
        If they don't match, then we raise an exception because something went wrong with how our client sent us their token.
        Next up is

        :param self: Access the class attributes and methods
        :param request: Request: Get the authorization header from the request
        :return: The payload of the access token
        :doc-author: Trelent
        """
        authorization_header = await self.get_authorization_header(request)
        if not authorization_header:
            return None

        self.check_prefix(authorization_header)
        payload = await get_payload_from_access_token(authorization_header)
        await validate_token(payload)
        return payload

    async def get_authorization_header(self, request):

        """
        The get_authorization_header function is a helper function that returns the authorization header from the request.
        If there is no authorization header, it returns None.

        :param self: Represent the instance of the class
        :param request: Get the authorization header from the request
        :return: The authorization header from the request
        :doc-author: Trelent
        """
        authorization_header = request.headers.get(self.authentication_header_name)
        if not authorization_header:
            return None
        return authorization_header

    def check_prefix(self, authorization_header):

        """
        The check_prefix function checks the prefix of the authorization header.
        The prefix is a string that indicates what type of authentication scheme is being used.
        In this case, we are using JWT so our prefix will be &quot;JWT&quot;. If it's not, then we raise an HTTPException.

        :param self: Represent the instance of the class
        :param authorization_header: Get the authorization header from the request
        :return: The prefix of the authorization header
        :doc-author: Trelent
        """
        prefix = authorization_header.split(' ')[0]
        if prefix != self.authentication_header_prefix:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid authentication scheme")


access_jwt_auth = JWTAuthentication()


def get_access_jwt_aut():

    """
    The get_access_jwt_aut function returns the access_jwt_auth variable.
        This is a JWT token that can be used to authenticate with the Spotify API.

    :return: The access_jwt_auth variable
    :doc-author: Trelent
    """
    return access_jwt_auth
