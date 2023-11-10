from fastapi import HTTPException, status, Request
from db.redis_db import get_redis_token_client
from db.mongo_db import get_db
from schemas.token import OtpToken
from schemas.users import UserCreate, UserLogin, UserBase, ResetPassword
from services.notification_httpx_client import get_notification_client
from utils.users import get_password_hash, verify_confirm_password, verify_password


class APIService:
    def __init__(self, redis_token_db, notification_client, get_mongo_db):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the redis and mongo databases for use in other functions.

        :param self: Represent the instance of the class
        :param redis_db: Connect to the redis database
        :param get_mongo_db: Get the mongodb database
        :return: A reference to the newly created object
        :doc-author: Trelent
        """
        self.redis_token_db = redis_token_db
        self.mongo_db = get_mongo_db
        self.notification_client = notification_client

    async def register_user(self, user: UserCreate):
        """
        The register_user function is used to register a new user.
            Args:
                user (UserCreate): The UserCreate object containing the information of the new user.

        :param self: Access the class itself, which is used to call other functions in the class
        :param user: UserCreate: Create a new user
        :return: The user_dict
        :doc-author: Trelent
        """
        await self.validate_user_register_info(user=user)
        try:
            hashed_password = get_password_hash(user.password)
            user.password = hashed_password
            user_dict = user.model_dump()
            user_dict.pop("confirm_password", None)
            await self.mongo_db["users"].insert_one(user_dict)
            user_dict['_id'] = str(user_dict['_id'])
            data = {"user_info": user_dict,
                    'message': 'Registration successful. Please check your email to activate your account.'}
            return data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an error occurred: {e}")

    async def confirm_token(self, token):
        email = await self.redis_token_db.get(f"registration_otp:{token}")
        if email:
            filter_query = {'email': email}
            update_query = {'$set': {'is_registered': True}}
            await self.mongo_db['users'].find_one_and_update(filter=filter_query, update=update_query)
            return {'message': 'Your account has been register Successfully'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': 'Your token  is invalid. Request another token'})

    async def send_registration_token(self, request: Request, user: UserBase):
        response = await self.notification_client.notification_register(email=user.email, request=request)
        data = {'message': 'Token has been Send. Please check your email to activate your account.'}
        if response.status_code == 200:
            return data
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    async def send_reset_password_token(self, request: Request, user: UserBase):
        response = await self.notification_client.notification_reset_password(email=user.email, request=request)
        data = {
            'message': 'Reset password Token has been Send. Please check your email to reset your account password.'}
        if response.status_code == 200:
            return data
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    async def change_password(self, token: OtpToken, passwords: ResetPassword, ):
        email = await self.redis_token_db.get(f"password_reset_token:{token.token}")
        if email:
            filter_query = {'email': email}
            update_query = {'$set': {'password': get_password_hash(passwords.password)}}
            await self.mongo_db['users'].find_one_and_update(filter=filter_query, update=update_query)
            return {'message': 'Your password has been changed Successfully'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': 'Your token  is invalid. Request another token'})

    async def login(self, form_data: UserLogin):
        """
        The login function is used to authenticate a user.
            It takes in the form data from the login page and checks if it matches with any of the users in our database.
            If there is no match, then an error message will be displayed on the screen.


        :param self: Represent the instance of the class
        :param form_data: UserLogin: Validate the user login
        :return: A user document
        :doc-author: Trelent
        """
        try:
            user = await self.mongo_db["users"].find_one({"email": form_data.email})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an error occurred: {e}")

        await self.validate_user_login(form_data=form_data, user=user)
        return user

    async def validate_user_register_info(self, user: UserCreate):
        """
        The validate_user_register_info function is used to validate the user's registration information.
            It checks if the email has already been registered, and if not, it verifies that the password and confirm_password fields match.

        :param self: Represent the class itself
        :param user: UserCreate: Validate the user's information
        :return: A 400 status code if the email is already registered
        :doc-author: Trelent
        """

        user_info = await self.mongo_db["users"].find_one({"email": user.email})
        if user_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': "Email already registered"})
        if not verify_confirm_password(user.password, user.confirm_password):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={'message': "Passwords must match!"})

    async def validate_user_login(self, form_data: UserLogin, user):
        """
        The validate_user_login_pass function is used to validate the user's login credentials.
            It takes in a form_data object and a user object as parameters. The function then checks if the
            password provided by the user matches that of their account, and raises an exception if it does not.

        :param self: Access the class attributes and methods
        :param form_data: UserLogin: Get the data from the form
        :param user: Pass the user object to the function
        :return: A user object if the username and password are correct
        :doc-author: Trelent
        """

        if user is None or not verify_password(form_data.password, user["password"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
        if not user['is_registered']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Your account hasn't been fully registered. please complete registration steps")


api_service = APIService(get_redis_token_client(), get_notification_client(), get_db())


def get_api_service():
    """
    The get_api_service function returns the api_service object.

    :return: The api_service object
    :doc-author: Trelent
    """
    return api_service
