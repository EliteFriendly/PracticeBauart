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



   
    
    
    return {"message": "answer"}


@app.post("/testAll")
def  sendToChequeInfo(file: UploadFile = File(...)):
    file_path = f"test-files/{file.filename}"
    with open(file_path, "wb") as tmpF:
        tmpF.write(file.file.read())
    QRreader.setQRImage(fileName=file_path)
    category=LLMproba.getCategory(listProducts=QRreader.getListProducts()["items"])
    listpr=LLMproba.getProductType(listProducts=QRreader.getListProducts()["items"])

    return {category: listpr}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        file_path = f"test-files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        return {"message": "File saved successfully"}
    except Exception as e:
        return {"message": e.args}
    

