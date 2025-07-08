from llama_cpp import Llama
import json


class AutoFillLLM:
    __llm = Llama.from_pretrained(
       	repo_id="bartowski/Ministral-8B-Instruct-2410-GGUF",
	    filename="Ministral-8B-Instruct-2410-Q4_K_S.gguf",
    )


    #Take name from all items in cheque
    def __getItems(self,jsonImput):
        productList = []
        for i in range(len(jsonImput.items)):
            productList.append(jsonImput.items[i]["name"])
        return productList


    def getCategory(self,jsonImput):
    
        listProducts = self.__getItems(jsonImput)#Get items from chequeInfo

        #Set initional information in LLM for distribution of categories
        response = self.__llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": f"Ты помощник учета финансов, твоя задача определить к какому виду расходов относится входящий чек {listProducts}.\
                    На вход поступает массив позиций товаров/услуг в чеке.\
                        У тебя имются следующие виды расходов:\
                            <Обязательные расходы> - к ним относится оплата квартиры, коммунальных платежей и т.д.;\
                            <Расходы на питание> - оплата продуктов в магазине, на рынке, питание в кафе, ресторанах, столовых и т.д.;\
                            <Расходы на хозяйственно бытовые нужды> - ремонт одежды, обуви  т.д., также покупка предметов личной гигиены;\
                            <Расхды на предметы личного пользования> - одежда, обувь, постельные принадлежности и т.д.;\
                            <Расходы на предметы быта> - мебель, светильники, часы, хрусталь и т.д..\
                                В качестве ответа выбери вид расходов и запиши это в category json. В случае если не все товары в чеке относится к одной категории,\
                                    то поставь доминирующию категорию расходов которых больше всего"
                    
            },
        
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"categoria":""},
                "required": ["categoria"],
            },
        },
        temperature=0.2#For small random from LLM
        )

        
        return json.loads(response["choices"][0]["message"]["content"])
    
    def getProductType(self,jsonImput):

        listProducts = self.__getItems(jsonImput)#Get items from chequeInfo

        #Set initional information in LLM for distribution of productType
        response = self.__llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": f"Ты помощник учета финансов, твоя задача определить к какому виду товаров/услуг относится каждый элемент входящего чека: {listProducts}.\
                    На вход поступает массив позиций товаров/услуг в чеке.\
                        У тебя нет фиксированных видов товаров/услуг, например: яблоко-продукты, джинсы-одежда, стрижка-парикмахерская, оперативная память - комплектующие компьютера, мыло - средства личной гигиены\
                                В качестве ответа напиши массив, который будет содежать к какому виду товаров/услуг относится каждый элемент чека и запиши это в json. В случае если не можешь определить вид товара/услуг,\
                                    то поставь: прочее/услуга"
                    
            },
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"productType":[{"type":"string"}]},
                "required": ["productType"],
            },
        },
        temperature=0.2
        )

        #Sometimes LLM distort the names of listItems, then take only values of keys
        js = list(json.loads(response["choices"][0]["message"]["content"]).values())

        #set productType in jsonImput
        for i in range(len(listProducts)):
            jsonImput.items[i]["productType"] = js[i]


        return jsonImput