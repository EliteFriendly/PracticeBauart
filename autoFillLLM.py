from llama_cpp import Llama
import json





class AutoFillLLM:
    __llm = Llama.from_pretrained(
       	repo_id="bartowski/Ministral-8B-Instruct-2410-GGUF",
	    filename="Ministral-8B-Instruct-2410-Q4_K_S.gguf",
    )


    def getCategory(self,listProducts):
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
            #{"role": "user", "content": listProducts},
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"categoria":""},
                "required": ["categoria"],
            },
        },
        )

        print(response["choices"][0]["message"]["content"][0])
        return (response["choices"][0]["message"]["content"])
    
    def getProductType(self,listProducts):
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
            #{"role": "user", "content": listProducts},
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"productType":[{"type":"string"}]},
                "required": ["productType"],
            },
        },
        )



        return response["choices"][0]["message"]["content"]