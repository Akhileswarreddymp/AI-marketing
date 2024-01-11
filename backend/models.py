import pydantic



class register_params(pydantic.BaseModel):
    username : str = pydantic.Field("",**{})
    email : str
    password : str


class otp_email(pydantic.BaseModel):
    email : str


class only_otp(pydantic.BaseModel):
    otp : str
    email : str


class login_params(pydantic.BaseModel):
    username : str
    password : str


class forgotPassword_params(pydantic.BaseModel):
    email : str
    otp : str
    newpassword : str
    confirm_Password : str
