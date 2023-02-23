from pydantic import BaseModel
from sklearn.pipeline import make_pipeline
import joblib
from fastapi import FastAPI, HTTPException
from Password_encoder import Chars_encoder
from uuid import uuid4, UUID
from typing import Optional
import random

class Stren(BaseModel):
    strength: str

class User_model(BaseModel):
    id: Optional[UUID] = uuid4()
    user_password: str

class Password_update(BaseModel):
    user_password: str


app = FastAPI()
LR_model = joblib.load('LogisticRegression_model.jl')
pass_history = []

@app.get('/password')
async def info():
    if len(pass_history) == 0:
        raise HTTPException(
            status_code=404,
            detail='Nothing was found'
        )
    else:
        return pass_history

@app.post('/password', response_model=Stren)
async def set_password(info: User_model):
    pipe = make_pipeline(
        Chars_encoder(), 
        LR_model
        )
    pas = info.dict()
    if ' ' in pas['user_password']:
        raise HTTPException(
            status_code = 400,
            detail = 'You cannot use spaces'
        )
    #if len(pas['user_password']) < 5:
    if len(pas.get('user_password')) < 5:
        raise HTTPException(
            status_code=400,
            detail='Lenght of your password must be greater than 4'
        )
    else:
        #password_container.append(pas)
        pred = pipe.predict(pas['user_password'])[0]
        pass_history.append(pas)
        if pred == 0:
            return {'strength': 'Weak'}
        if pred == 1:
            return {'strength': 'Medium'}
        if pred == 2:
            return {'strength': 'Strong'}
    
@app.delete('/password/{user_id}')
async def delete_info(user_id: UUID):
    for user in pass_history:
        if user['id'] == user_id:
            pass_history.remove(user)
            raise HTTPException(
                status_code=200,
                detail='User was removed'
            )
        raise HTTPException(
            status_code=404,
            detail=f'User with id {user_id} was not found'
        )

@app.put('/passwor/{user_id}')
async def update_password(pas_update: Password_update, user_id: UUID):
    new_pas = pas_update.dict()
    for user in pass_history:
        if user_id == user['id']:
            if len(new_pas.get('user_password')) < 5:
                raise HTTPException(
                    status_code=400,
                    detail='Lenght of your password must be greater than 4'
                )
            user['user_password'] = new_pas.get('user_password')
            raise HTTPException(
                status_code=200,
                detail='Password was updated'
            )
        return
