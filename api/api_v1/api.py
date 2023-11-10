from bson import ObjectId
from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.security import HTTPBearer
from pymongo import ReturnDocument
from starlette import status

from db.mongo_db import get_db
from schemas.token import OtpToken
from schemas.users import UserCreate, UserLogin, UserBase, ResetPassword
from services.api_services import APIService, get_api_service
from services.authentication import get_access_jwt_aut

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, api_service: APIService = Depends(get_api_service)):
    """
    The register_user function creates a new user in the database.

    :param user: UserCreate: Pass the user object to the function
    :param api_service: APIService: Pass in the apiservice class that is defined in api_service
    :return: A dictionary with a user key
    :doc-author: Trelent
    """
    user_dict = await api_service.register_user(user)
    return {'user': user_dict}


@router.post('/confirm_token')
async def confirm_token(token: OtpToken, api_service: APIService = Depends(get_api_service)):
    response = await api_service.confirm_token(token=token.token)
    return response


@router.post("/send_registration_token", status_code=status.HTTP_200_OK)
async def send_registration_token(request: Request, user: UserBase, api_service: APIService = Depends(get_api_service)):
    return await api_service.send_registration_token(request, user)


@router.post("/send_reset_password_token", status_code=status.HTTP_200_OK)
async def send_reset_password_token(request: Request, user: UserBase,
                                    api_service: APIService = Depends(get_api_service)):
    return await api_service.send_reset_password_token(request, user)


@router.post('/change_password', status_code=status.HTTP_200_OK)
async def change_password(token: OtpToken, passwords: ResetPassword,
                          api_service: APIService = Depends(get_api_service)):
    return await api_service.change_password(token=token, passwords=passwords)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: UserLogin, api_service: APIService = Depends(get_api_service)):
    """
    The login function takes in a UserLogin object and returns the user_id of the logged-in user.
        The login function is called when a POST request is made to /login with form data containing
        username and password fields.

    :param form_data: UserLogin: Validate the request body
    :param api_service: APIService: Inject the apiservice instance into the function
    :return: A dictionary with the user_id
    :doc-author: Trelent
    """
    user = await api_service.login(form_data=form_data)
    return {"user_id": str(user['_id'])}


@router.patch('/update_profile', status_code=status.HTTP_200_OK)
async def update_profile(update_user_info: dict, db=Depends(get_db),
                         payload: HTTPBearer = Depends(get_access_jwt_aut())):
    """
    The update_profile function updates the user's profile information.
        The function takes in a dictionary of key-value pairs that will be updated in the database.
        The function returns a message and the result of updating the user's profile.

    :param update_user_info: dict: Get the data from the request body
    :param db: Get the database connection
    :param payload: HTTPBearer: Get the access token from the header
    :return: A dict with a message and the result of the update
    :doc-author: Trelent
    """
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required for this API")

    updated_user = await db['users'].find_one_and_update(
        filter={'_id': ObjectId(user_id)},
        update={'$set': update_user_info},
        projection={"_id": 0, "password": 0},
        return_document=ReturnDocument.AFTER)

    return {'message': 'User has been updated successfully', 'result': updated_user}
