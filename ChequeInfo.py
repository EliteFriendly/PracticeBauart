import requests
import json
import pandas as pd
import os



class ChequeInfo:
    __goodIMGExtension = (".jpg",".pdf",".png",".jpeg",)
    __token = os.getenv("TOKEN") # token from website: https://proverkacheka.com 
    __websiteAPI = os.getenv("API") #API to get info from cheques from website

    __columnsName = ("name","productType","quantity","price","sum","data",)
    __listProducts = pd.DataFrame(columns=__columnsName) 
    '''
    price in next format: 300.50, where 300 its rubles, and 50 its pennies.
    data in next format: YYYY-MM-DD HH:MM:SS
    productType: can be type from productType.txt
    '''


    def setQRImage(self,fileName = ""):
        typeIMG = False
        for i in range(len(self.__goodIMGExtension)):# Checking the file type
            if not self.__goodIMGExtension[i] in fileName:
                 typeIMG = True
       
        if not typeIMG:
            raise NameError("Wrong file type, can be only: .jpg, .pdf, .png, .jpeg")

        files = {"qrfile": open(fileName, "rb")}# For set image to API

        data = {
        "token": self.__token,
         }
        r = requests.post(url=self.__websiteAPI, data=data, files=files)
        
        for i in range(len(r.json()["data"]["json"]["items"])):# take only items/products from .json and set its into a DataFrame
            tmp = []
            tmp.append(r.json()["data"]["json"]["items"][i]["name"])
            tmp.append("None")
            tmp.append(r.json()["data"]["json"]["items"][i]["quantity"])
            tmp.append(r.json()["data"]["json"]["items"][i]["price"]/100.0)
            tmp.append(tmp[2]*tmp[3])
            tmp.append(r.json()["data"]["json"]["dateTime"])
             
            self.__listProducts.loc[-1] = tmp
            self.__listProducts.index = self.__listProducts.index + 1 
        
    
    def getListProducts(self):
        return self.__listProducts.sort_index()
            
