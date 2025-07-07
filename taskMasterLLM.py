from llama_cpp import Llama
import json



class TaskMasterLLM:
    __llm = Llama.from_pretrained(
       	repo_id="bartowski/Ministral-8B-Instruct-2410-GGUF",
	    filename="Ministral-8B-Instruct-2410-Q4_K_S.gguf",
    )
    
    
    
    def getPlan(self,task,description):
        
        response = self.__llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": f"Ты помогаешь мне составить план для достижения цели, я поставил себе следующую цель на день: <{task}>. \
                    Также сформировал следующее описание, чтобы конкретизировать цель: <{description}>.\
                    На вход поступает моя цель и описание к ней. Я хочу чтобы ты составил шаги к её достижению, но чтобы это можно было сделать за день\
                    Предлагай мне шаги которые может сделать обычный человек, и постарайся не сводить к банальному: купи или заработай деньги и купи.\
                    Я хочу чтобы шаги были довольно подробно описаны.\
                        В качестве ответа создай мне массив шагов для достижения цели в поле steps в файл типа json.\
                            В случае если данная цель является невозможной для обычного человека то поле category напиши <I> "
                    
            },
            #{"role": "user", "content": listProducts},
        ],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {"steps":[{"type":"string"}]},
                
                #"type":"object",
                #"properties":{"category":{"type":"string"}}
                
                
                "required": ["steps"],

            },
        },
        temperature=0.8
        )
        
        
        
        
        return json.loads(response["choices"][0]["message"]["content"])