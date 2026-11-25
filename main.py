from datetime import datetime, timedelta
from email.mime import message

import jwt
from fastapi import FastAPI, HTTPException
SECRET_KEY="56768434"
ALGORITHM="HS256"
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



