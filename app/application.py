from fastapi import FastAPI, File, Form, UploadFile
from fastapi.datastructures import UploadFile
from schema import ResponseSchema
#from mangum import Mangum
import uvicorn
from business_card_ocr import BusinessCardOCR

tags_metadata = [
  {
    "name": "business_card_ocr",
    "description": "Read business card and output related details, eg. name, email, contact, address"
  }
]

business_card_ocr = BusinessCardOCR()

app = FastAPI(
  title = "Business Card OCR",
  description = "Reads and recognises information on business card",
  version = "0.0.1",
  openapi_tags=tags_metadata
)

@app.get("/")
def hello():
  return {"message": "Welcome to business card recogniser"}

@app.post("/recognise", tags=["business_card_ocr"], response_model=ResponseSchema) 
def recognise_business_card(file: UploadFile = File(...)) -> ResponseSchema:
  success = False
  message = ''
  success, message, data = business_card_ocr.analyse_file(file)
  response = {'success': success, 'message': message, 'data': data}
  return response

#handler = Mangum(app)

if __name__ == '__main__':
  uvicorn.run('application:app', host='127.0.0.1', port=8000, reload=True)
