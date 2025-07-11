from fastapi import FastAPI, UploadFile, File, APIRouter,HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from ChequeInfo import ChequeInfo
from pydantic import BaseModel, Field

#TODO Такая же ситуация с модулем, продумай структуру, перенеси в другую папку


uploadIMG = APIRouter(prefix = "/api/qr_put",tags=["Send this into a API wich take items from cheque"])
QRreader = ChequeInfo()


#TODO Так же отдельный файл с моделями для валидации
#Thing which uses to send info in ChequeInfo
class ReqImgLLM(BaseModel):
    userToken: str = Field(description="Token?")
    userID: int = Field(default=...)
    qrInfo: str = Field(description="Info/code getted by scanning cheque")




#TODO Так же перенеси в отдельный файл и добавь middleware для проверки токена, и наследуй его в класс
#   кстати не факт что такая функция нужна после того как она в основной бэк интегрирована
@uploadIMG.post("/uploadIMG")
def  sendToChequeInfo(file:UploadFile):
    #Save file
    file_path = f"test-files/{file.filename}"
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    
    #Send information from cheque to LLM
    QRreader.setQRImage(fileName=file_path)
    return {"message": "File saved successfully"}
    

@uploadIMG.get("/showProductsList")
def getProductList():
    return QRreader.getDistProducts()

