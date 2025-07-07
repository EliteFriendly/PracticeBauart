from fastapi import FastAPI, UploadFile, File, APIRouter
from ChequeInfo import ChequeInfo
from pydantic import BaseModel, Field


#Thing which uses to send info in ChequeInfo
class ReqImgLLM(BaseModel):
    userToken: str = Field(description="Token?")
    userID: int = Field(default=...)
    qrInfo: str = Field(description="Info/code getted by scanning cheque")



uploadIMG = APIRouter(prefix = "/api/autofill_llm",tags=["Send this into a AutoFillLLM"])
QRreader = ChequeInfo()

@uploadIMG.post("/uploadIMG")
def  sendToChequeInfo(file:UploadFile, reqImgLLM: ReqImgLLM):
    #Save file
    file_path = f"test-files/{file.filename}"
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    
    #Send information from cheque to LLM
    QRreader.setQRImage(fileName=file_path)
    return {"message": "File saved successfully"}
    
@uploadIMG.get("/showProductsList")
def getProductList():
    return QRreader.getDictProducts(QRreader)

