from fastapi import FastAPI, UploadFile, File
from uploadIMGRoute import uploadIMG
from autoFillLLM import AutoFillLLM
from ChequeInfo import ChequeInfo
import json

app = FastAPI()
QRreader = ChequeInfo()
app.include_router(uploadIMG)
LLMproba = AutoFillLLM()

@app.get("/")
def root():

    category = LLMproba.getCategory(listProducts=["Яблоко"])
     
   
    
    print(category.items())
    return {category}


@app.post("/testAll")
def  sendToChequeInfo(file: UploadFile = File(...)):
    file_path = f"test-files/{file.filename}"
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    QRreader.setQRImage(fileName=file_path)
    listProducts=QRreader.getListProducts()
    positions =[]
    for i in range(len(QRreader.getListProducts()["items"])):
        positions.append(QRreader.getListProducts()["items"][i]["name"])
   
   
    category=LLMproba.getCategory(positions)
    listpr=LLMproba.getProductType(positions)
    #return listProducts
    return [category,listpr]


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        file_path = f"test-files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        return {"message": "File saved successfully"}
    except Exception as e:
        return {"message": e.args}
    

