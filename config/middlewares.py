from sqlalchemy import false
from userService.v1.controllers import UserController
from fastapi import Depends, Request, status, HTTPException
from config.config import AuthJWT
import re


async def is_authenticated(request: Request, TokenHandler: AuthJWT = Depends()):
    try:
        TokenHandler.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))


async def is_owner(request: Request, TokenHandler: AuthJWT = Depends()):
    TokenHandler.jwt_required()
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if user.category != "owner" and user.category != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user


async def is_driver(request: Request, TokenHandler: AuthJWT = Depends()):
    TokenHandler.jwt_required()
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if user.category != "driver" and user.category != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user


async def is_superuser(request: Request, TokenHandler: AuthJWT = Depends()):
    TokenHandler.jwt_required()
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if user.category != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user
