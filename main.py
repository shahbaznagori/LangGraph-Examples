print("--- SCRIPT INITIALIZED ---", flush=True)
from mem0 import Memory
print("Mem0 imported")
from dotenv import load_dotenv
print("Dotenv imported")
from groq import Groq
print("Groq imported")
from pydantic import BaseModel
print("Pydantic imported")
from .config import CONFIG 
print("Before env")
load_dotenv()
print("Env loaded")
import json


#Mem0 OSS + Qdrant (Vector Database)
config = {
    "llm":{
    "provider": "openai",
    "config":{
        # "model": "openrouter/free",
        "model": "nex-agi/nex-n2.5-pro:free",
        
"api_key": CONFIG.get("llm").get("api_key"),
        "openai_base_url": "https://openrouter.ai/api/v1",
 

    }
    },
            "embedder": {
        "provider": "openai",
        "config": {
        "model": "openai/text-embedding-3-small",
            # "api_key": CONFIG.get("embedder").get("api_key"), # Your OpenRouter Key
        "api_key": CONFIG.get("embedder").get("api_key"),
        "openai_base_url": "https://openrouter.ai/api/v1"

        }
    },

    "vector_store":{
        "provider":"qdrant",
        "config":{
            "url":"https://5ba63ce8-cb73-4a06-acfd-8e7493014290.sa-east-1-0.aws.cloud.qdrant.io",
            "api_key": CONFIG.get("vector_db").get("api_key"),
            "collection_name": "mem0_test_1536"

        }
    },
    
    
}




mem_client = Memory.from_config(config)
print("config loaded")

print("Update method:", mem_client.update)
    

#Groq Layer
client = Groq()
print("Groq client initialized")
#Using fastapi

class ChatRequest(BaseModel):
    user_id: str
    message: str



# @app.post("/chat")
# def chat(request:ChatRequest):
while True:
    user_query = input("Ask something>>>")
    
    search_memory = mem_client.search( #it will only search for relevent memories.
        query=user_query,
        filters={
            "user_id":"convo-1"
        }
    )
    
    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}" 
        for mem in search_memory.get("results",[])
    ]
    
    print("Fount memories:", memories)
    
    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    
    When comparing new information with existing memories:

    - If the information is completely new → ADD.
    - If the new information changes or contradicts an existing memory → UPDATE the existing memory.
    - Do NOT ADD a second memory when an existing memory describes the same preference.
    - If the new information explicitly reverses an existing preference, replace the old preference with the new one.
    - Always prefer UPDATE over ADD when an existing memory concerns the same subject.
    - Use the existing memory ID for UPDATE.
    """
    
    response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
             {
               "role":"system",
               "content":SYSTEM_PROMPT
             },    
            {
                "role":"user",
                "content":user_query
            },
            ]

    )
    ai_response = response.choices[0].message.content
    print("\nAI Response:", ai_response)

    reseult = mem_client.add(
    user_id="convo-1",
    messages=[
    {"role": "user", "content": user_query}
    ]
    )
    print(mem_client.update)
    print("Memory has been saved",reseult)

    
     