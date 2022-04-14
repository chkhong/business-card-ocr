from pydantic import BaseModel
from fastapi import Query, File, Form, UploadFile

class ResponseSchema(BaseModel):
  success: bool = False
  message: str = Query(None, title="Error message is printed here if error occurs")
  data: dict = Query(None, title="Data returned here if success")
