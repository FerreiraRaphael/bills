from typing import Dict
from typing_extensions import Annotated, Doc
from typing import Any
from jwt.algorithms import RSAAlgorithm
import jwt
import aiohttp
from fastapi import Request, status
from fastapi.exceptions import HTTPException

from api_py.env import get_env

CLERK_FRONTEND_API_URL = get_env("CLERK_FRONTEND_API_URL")

class AuthenticationFailed(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)

def authenticate(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        raise AuthenticationFailed("Bearer token not provided.")
    user = decode_jwt(token)
    if not user:
        raise AuthenticationFailed("Invalid token")
    yield user

async def decode_jwt(http: aiohttp.ClientSession, token: str):
    jwks_data = await get_jwks()
    public_key = RSAAlgorithm.from_jwk(jwks_data["keys"][0])
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_signature": True},
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired.")
    except jwt.DecodeError as e:
        raise AuthenticationFailed("Token decode error.")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token.")

    user_id = payload.get("sub")
    if user_id:
        # user, created = User.objects.get_or_create(username=user_id)
        return user_id
    return None


# class JWTAuthenticationMiddleware():

# def fetch_user_info(http: aiohttp.ClientSession, user_id: str):
#     async with http.get()
#     response = requests.get(
#         f"{CLERK_API_URL}/users/{user_id}",
#         headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
#     )
#     if response.status_code == 200:
#         data = response.json()
#         return {
#             "email_address": data["email_addresses"][0]["email_address"],
#             "first_name": data["first_name"],
#             "last_name": data["last_name"],
#             "last_login": datetime.datetime.fromtimestamp(
#                 data["last_sign_in_at"] / 1000, tz=pytz.UTC
#             ),
#         }, True
#     else:
#         return {
#             "email_address": "",
#             "first_name": "",
#             "last_name": "",
#             "last_login": None,
#         }, False


async def get_jwks(http: aiohttp.ClientSession):
  async with http.get(f"{CLERK_FRONTEND_API_URL}/.well-known/jwks.json") as res:
      if res.status == 200:
          jwks_data = await res.json()
          return jwks_data
      else:
          raise AuthenticationFailed("Failed to fetch JWKS.")


# import aiohttp
# import asyncio

# async def main():

#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://python.org') as response:

#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])

#             html = await response.text()
#             print("Body:", html[:15], "...")

# asyncio.run(main())
