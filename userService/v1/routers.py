from fastapi import APIRouter, Response, status, HTTPException
from userService.v1.schemas import UserLogin, UserSignup, AuthToken, AccessToken
from userService.v1.models import User
from userService.v1.controllers import UserController
from config.config import AuthJWT
from config.deps import get_controller
from fastapi import Depends
from config.middlewares import is_authenticated


userrouter = APIRouter(prefix="/users", tags=["users"])


@userrouter.post("/register", response_model=AuthToken, status_code=201)
async def createUser(
    request: UserSignup,
    response: Response,
    TokenHandler: AuthJWT = Depends(),
    userController: UserController = Depends(get_controller(UserController)),
):
    if await userController.check_user_by_phone(request.mobile_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given phone number already exists",
        )
    if not userController.validate_mobile_number(request.mobile_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number invvalid",
        )
    if not userController.validate_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="password should be at leasts 8 letter long and should have atleast one lowercase ,one upper case and one special character ",
        )
    userid = await userController.create_user(request.dict())
    return await userController.create_user_tokens(TokenHandler, userid)


@userrouter.post("/login", response_model=AuthToken, status_code=200)
async def loginUser(
    request: UserLogin,
    response: Response,
    TokenHandler: AuthJWT = Depends(),
    userController: UserController = Depends(get_controller(UserController)),
):
    if not (user := await userController.authenticate_user(**request.dict())):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="either password or mobile_number is incorrect",
        )
    return await userController.create_user_tokens(TokenHandler, user.id)


@userrouter.post("/refresh/token", response_model=AccessToken, status_code=200)
async def refreshToken(
    response: Response,
    TokenHandler: AuthJWT = Depends(),
    user: User = Depends(is_authenticated),
    userController: UserController = Depends(get_controller(UserController)),
):
    return userController.create_access_token(TokenHandler, user.id)
