from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.auth import create_access_token

auth_routes = APIRouter(prefix='/api/auth', tags=['auth'])


@auth_routes.post('/token')
def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username != 'die711':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')

    token = create_access_token({'username': username})

    return {
        'access_token': token
    }
