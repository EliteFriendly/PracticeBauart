from fastapi import FastAPI, UploadFile, File, APIRouter
from ChequeInfo import ChequeInfo

uploadIMG = APIRouter()
QRreader = ChequeInfo

@uploadIMG.post("/uploadIMG")
def  sendToChequeInfo(file: UploadFile = File(...)):
    file_path = f"test-files/{file.filename}"
    QRreader.setQRImage(QRreader,fileName=file_path)
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    return {"message": "File saved successfully"}
    
@uploadIMG.get("/showProductsList")
def getProductList():
    return QRreader.getListProducts(QRreader)

