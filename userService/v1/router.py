from fastapi import APIRouter, Response, status, HTTPException
from userService.v1.schemas import UserLogin, UserSignup, AuthToken, AccessToken
from userService.v1.controllers import User
from config.config import AuthJWT
from fastapi import Depends


userrouter = APIRouter(prefix="/users", tags=["users"])


@userrouter.post("/register", response_model=AuthToken, status_code=201)
async def createUser(
    request: UserSignup, response: Response, TokenHandler: AuthJWT = Depends()
):
    try:
        if await User.check_user_by_phone(request.mobile_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with given phone number already exists",
            )
        if not User.validate_mobile_number(request.mobile_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number invvalid",
            )
        if not User.validate_password(request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password should be at leasts 8 letter long and should have atleast one lowercase ,one upper case and one special character ",
            )
        userid = await User.create_user(request.dict())
        return await User.create_user_tokens(TokenHandler, userid)

    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="failed to create user",
        )


@userrouter.post("/login", response_model=AuthToken, status_code=200)
async def loginUser(
    request: UserLogin, response: Response, TokenHandler: AuthJWT = Depends()
):
    if not (user := await User.authenticate_user(**request.dict())):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="either password or mobile_number is incorrect",
        )
    return await User.create_user_tokens(TokenHandler, user.id)


@userrouter.post("/refresh/token", response_model=AccessToken, status_code=200)
async def refreshToken(response: Response, TokenHandler: AuthJWT = Depends()):
    try:
        TokenHandler.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    userid = TokenHandler.get_jwt_subject()
    return await User.create_access_token(TokenHandler, userid)
