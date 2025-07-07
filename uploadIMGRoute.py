from fastapi import FastAPI, UploadFile, File, APIRouter
from ChequeInfo import ChequeInfo
from pydantic import BaseModel, Field


#Thing which uses to send info in ChequeInfo
class ReqImgLLM(BaseModel):
   # qrImg: UploadFile = Field(default=...,description="Файл с qr-кодом чека")
    userID: int = Field(default=...)
    qrInfo: str = Field(description="Информация с чека")



uploadIMG = APIRouter(prefix = "/api/autofill_llm",tags=["Отправка чека для дальнейшего заполнения в бд"])
QRreader = ChequeInfo()

@uploadIMG.post("/uploadIMG")
def  sendToChequeInfo(file:UploadFile,reqImgLLM: ReqImgLLM):
    file_path = f"test-files/{file.filename}"
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    QRreader.setQRImage(fileName=file_path)
    return {"message": "File saved successfully"}
    
@uploadIMG.get("/showProductsList")
def getProductList():
    return QRreader.getDictProducts(QRreader)

