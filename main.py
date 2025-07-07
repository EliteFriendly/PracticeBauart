from fastapi import FastAPI, UploadFile, File
from uploadIMGRoute import uploadIMG
from autoFillLLM import AutoFillLLM
from ChequeInfo import ChequeInfo

app = FastAPI()
QRreader = ChequeInfo()
app.include_router(uploadIMG)
LLMproba = AutoFillLLM()

@app.get("/")
def root():
    return {"Main Page"}
#Test

@app.post("/testAll")
def  sendToChequeInfo(file: UploadFile = File(...)):
    file_path = f"test-files/{file.filename}"
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    QRreader.setQRImage(fileName=file_path)
    positions =[]
    for i in range(len(QRreader.getListProducts()["items"])):
        positions.append(QRreader.getListProducts()["items"][i]["name"])
   
   
    category=LLMproba.getCategory(positions)
    listpr=LLMproba.getProductType(positions)
    return [category,listpr]


    

