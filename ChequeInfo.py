import requests, json
import os




class ChequeInfo():
    __goodIMGExtension = ("bmp", "gif", "jpeg", "png", "tiff", "pdf",)
    __token = os.getenv("TOKEN") # token from website: https://proverkacheka.com 
    __websiteAPI = os.getenv("API") #API to get info from cheques from website


    __columnsName = ("name","productType","quantity","price","sum",)
    __dictProducts = {
        "items":[],
        "data":""
    } 
    '''
    price in next format: 300.50, where 300 its rubles, and 50 its pennies.
    data in next format: YYYY-MM-DDTHH:MM:SS, where T - special symbol from API
    productType: can be type from productType.txt
    '''


    def setQRImage(self,fileName = ""):
               
        typeIMG = False
        for i in range(len(self.__goodIMGExtension)):# Checking the file type
            if not self.__goodIMGExtension[i] in fileName:
                 typeIMG = True
       
        if not typeIMG:
            raise NameError("Wrong file type, can be only: bmp, gif, jpeg, png, tiff, pdf")

        files = {"qrfile": open(fileName, "rb")}# For set image to API

        data = {
        "token": self.__token,
         }
        r = requests.post(url=self.__websiteAPI, data=data, files=files)
        
        #If was error from request
        if not (r.json()["code"] == 1):
            codeError = r.json()["code"]
            with open('data_failed.json', 'w') as outfile:
                json.dump(r.json(), outfile)
            raise NameError (f"Error cheque read, error:{codeError}") 
            '''
            You can watch code error in: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fproverkacheka.com%2Ffiles%2Fhelp%2Fdocumentation_api.docx&wdOrigin=BROWSELINK
            But also code-3 can be code-0 or code-2
            '''
        
        
        #Get info from dict, for future update __dictProducts
       
        tmp = []
        for i in range(len(r.json()["data"]["json"]["items"])):# take only items/products from .json and set its into a tmp array
            tmp.append(r.json()["data"]["json"]["items"][i]["name"])
            tmp.append("None")
            tmp.append(r.json()["data"]["json"]["items"][i]["quantity"])
            tmp.append(r.json()["data"]["json"]["items"][i]["price"]/100.0)
            tmp.append(tmp[2]*tmp[3])
            self.__dictProducts["items"].append( { k:v for (k,v) in zip(self.__columnsName, tmp)}  )
            tmp = []
        
        #Update __dictProducts
    
        self.__dictProducts["data"] = r.json()["data"]["json"]["dateTime"]
        

        
    
    def getListProducts(self):
        return self.__dictProducts
            
