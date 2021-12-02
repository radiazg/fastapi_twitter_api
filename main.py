# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr, Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, From, Path


app = FastAPI()

# Models

class PasswordMixin(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=15,
        example='password'
    )

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(
        ..., 
        example='ricardo@exmaple.com'
    )

class UserLogin(UserBase, PasswordMixin):
    pass

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Ricardo'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Diaz'
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User, PasswordMixin):
    pass

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example='This tweet is a example for FastAPI'
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(
    user: UserRegister = Body(...)
):
    """
    ## Signup a User

    This path operation register a user in the app

    **Parameters**

    - Request body parameter
        - user: UserRegister

    Return a json with the basic user information:

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    
    #open file user.json in read/write mode with utf-8 encoding
    with open("users.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # transform the request body in dictionary and save in variable dict
        user_dict = user.dict()
        # user_id and birth_date are not string and use cast for transform in dict
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        # add user dictionary to results variable
        results.append(user_dict)

        # move the firts line in file
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))
        return user

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    """
    ## login a User

    This path operation login a user in the app

    **Parameters**

    - Request Form parameter
        - username: srt -> A user name
        - password: str -> A password for user name

    Return a json with the basic user information:

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    pass

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    ## Show all users

    This path operation show all users in the app

    **Parameters**

    - 

    Return a json list with all users in the app with following keys:

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_a_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweet"]
)
def home():
    """
    ## Show all tweets

    This path operation show all tweets in the app

    **Parameters**

    - 

    Return a json list with all tweets in the app with following keys:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: User
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweet"]
)
def post(tweet: Tweet = Body(...)):
    
    """
    ## Post a Tweet

    This path operation post a tweet in the app

    **Parameters**

    - Request body parameter
        - tweet: Tweet

    Return a json with the basic tweet information:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: User
    """
    #open file tweets.json in read/write mode with utf-8 encoding
    with open("tweets.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # transform the request body in dictionary and save in variable dict
        tweet_dict = tweet.dict()
        # tweet_id, created_at and update_at are not string and use cast for transform in dict
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        # user_id and birth_date are not string and use cast for transform in dict
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        # add user dictionary to results variable
        results.append(tweet_dict)

        # move the firts line in file
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweet"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweet/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweet"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweet/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweet"]
)
def update_a_tweet():
    pass