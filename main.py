from fastapi import FastAPI, UploadFile, File
from uploadIMGRoute import uploadIMG
from fillLLMRoute import  productsLLM
#from autoFillLLM import AutoFillLLM
from ChequeInfo import ChequeInfo

app = FastAPI()
#QRreader = ChequeInfo()
app.include_router(uploadIMG)
app.include_router(productsLLM)
#LLMproba = AutoFillLLM()


@app.get("/")
def root():

    return {"Main page"}
#Test



    

