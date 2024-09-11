from pydantic import BaseModel

class BlogPost(BaseModel):
    title: str
    text: str
    user_id: str

    


class UserLogin(BaseModel):
    username: str
    password: str