from sqlalchemy import false
from userService.v1.controllers import UserController
from busService.v1.controllers import BusController
from fastapi import (
    Depends,
    Request,
    status,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from config.config import AuthJWT
import re


async def is_authenticated(request: Request, TokenHandler: AuthJWT = Depends()):
    try:
        TokenHandler.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))


async def is_owner(request: Request, TokenHandler: AuthJWT = Depends()):
    try:
        TokenHandler.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if user.category != "owner" and user.category != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user


async def is_driver(request: Request, TokenHandler: AuthJWT = Depends()):
    try:
        TokenHandler.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if user.category != "driver" and user.category != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user


async def is_superuser(request: Request, TokenHandler: AuthJWT = Depends()):
    try:
        TokenHandler.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if user.category != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user


async def is_owner_or_driver(
    request: Request, TokenHandler: AuthJWT = Depends()
):
    try:
        TokenHandler.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    user = await (UserController.get_user_by_id(TokenHandler.get_jwt_subject()))
    if (
        user.category != "owner"
        and user.category != "driver"
        and user.category != "superuser"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized",
        )
    return user


async def is_bus_or_authenticated_req(
    request: Request, TokenHandler: AuthJWT = Depends()
):
    try:
        TokenHandler.jwt_required()
    except Exception as e:
        return "unverified"
    subject = TokenHandler.get_jwt_subject()
    if "__" in str(subject):
        bus_id, bus_number = subject.split("__")
        if not (bus := await BusController.get_bus_by_id(int(bus_id))):
            return "unverified"
        if bus.bus_number != bus_number or bus.token != TokenHandler._token:
            return "unverified"
        return "owner"
    user = await (UserController.check_user_by_id(subject))
    if not user:
        return "unverified"
    return "user"


async def is_bus_or_authenticated(
    websocket: WebSocket, token: str, TokenHandler: AuthJWT = Depends()
):
    try:
        TokenHandler.jwt_required("websocket", token=token)
    except Exception as e:
        return "unverified"

    subject = TokenHandler.get_raw_jwt(token)["sub"]
    if "__" in str(subject):
        bus_id, bus_number = subject.split("__")
        if not (bus := await BusController.get_bus_by_id(int(bus_id))):
            return "unverified"
        if bus.bus_number != bus_number or bus.token != token:
            return "unverified"
        return "owner"

    user = await (UserController.check_user_by_id(subject))
    if not user:
        return "unverified"
    return "user"
