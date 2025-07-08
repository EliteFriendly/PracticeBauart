from fastapi import APIRouter,HTTPException
from autoFillLLM import AutoFillLLM
from pydantic import BaseModel, Field
import os
from jose import jwt



productsLLM = APIRouter(prefix = "/api/autofill_llm",tags=["Send this into a AutoFillLLM"])
autoFillLLM = AutoFillLLM()


#Thing which uses to send info in autoFillLLM, especially items from cheque
class ReqProductsLLM(BaseModel):
    userToken: str = Field(default=...,description="Access token")
    userID: int = Field(default=...)
    items: list = [
        {"name": str,  
        "productType": str,
        "quantity": int,
        "price": float,
        "sum": float}
        ]


def tokenVerification(token,userId):
    secretKey = os.getenv("SECRET_KEY")
    try:
        deCode = jwt.decode(token=token, key=secretKey, algorithms="HS256")
        if(deCode!=userId):#?
            raise HTTPException(status_code=401, detail="Invalid token") 
    except Exception:
        raise HTTPException(status_code=401, detail="Expired token")



#Router
@productsLLM.post("/setCategory")
def sendToChequeInfo(reqProductsLLM: ReqProductsLLM):
    categories = autoFillLLM.getCategory(reqProductsLLM)
    return categories


@productsLLM.post("/setProductsTypes")
def sendToChequeInfo(reqProductsLLM: ReqProductsLLM):
    productType = autoFillLLM.getProductType(reqProductsLLM)
    return productType



