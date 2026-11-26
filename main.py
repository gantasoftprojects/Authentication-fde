from datetime import datetime, timedelta
from email.mime import message

import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY="56768434"
ALGORITHM="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#====================================
# step2 Dummy Database
# ===================================
users={
    "ravi":{
        "username":"ravi",
        "password":"ravi@123",
        "email":"ravi@gantasoft.com",
        "role":"student"
    },
    "suresh":{
        "username":"suresh",
        "password":"suresh@g123",
        "email":"suresh@gantasoft.com",
        "role":"Trainer"
    }
}

# step 1
app=FastAPI()

@app.get("/")
async def root():
    return {"message": "jwt example "}


# step-4 create_access_token
def create_access_token(username: str, role: str):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    token= jwt.encode(
       payload,
       SECRET_KEY,
       algorithm=ALGORITHM
    )
    return token

# step-3 --> login route
@app.post("/login")
async def login(username:str,password:str):
  user=users.get(username)
  if user is None:
      raise HTTPException(status_code=401,message="User Not Foud")
  if user["password"] != password:
      raise HTTPException(status_code="401",message="Enter valid credials")

  token=create_access_token(user["username"],user["role"])
  return {"access_token":token,"token_type":"bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username=payload["username"]
        if username is None:
            raise HTTPException(status_code=401, detail="InValid")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="InValid Token Exp")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="InValid Token")

def get_access(role:str):
    if role != "student":
        raise HTTPException(status_code=401, detail="you don't have permission")


def trainer_only(role:str):
    if role != "Trainer":
        raise HTTPException(status_code=401, detail="you don't have permission")


@app.get("/profile")
def get_current_user(user: str = Depends(get_current_user)):

    return {"message":"User Profile Access ",
        "username":user["username"],
        "role":user["role"]
    }


@app.get("/videos")
def get_videos(user: str = Depends(get_current_user)):
    # get_access(user["role"])
    return {"videos":[]}

@app.post("/videos")
def upload_video(user: str = Depends(get_current_user)):
    trainer_only(user["role"])
    return {"message":"video upload"}



