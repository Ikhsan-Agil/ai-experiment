import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # If env config not provided, please use Bailian API KEY: api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

print('Halo saya Qwen, asisten virtual kamu.....\nIya kamu \U0001F60A \nSilakhan tanyakan sesuatu.')

messages = [
    # {
    #     "role": "system",
    #     "content": "Kamu adalah Hitler. kalo ada yg tanya hal selain tentang Hitler tolong bilang 'Maaf, saya Hitler. Saya tidak tau hal tersebut'. Apabila ada yang bertanya dengan bahasa selain Bahasa Indonesia, tolong jawab dengan 'Maaf, saya hanya mengerti bahasa Indonesia'"
    # }
]

def inputs():
    content = input("Tanyakan Sesuatu (Ketikkan 'keluar' untuk keluar): ")

    content_input = content.encode('utf-8').decode('unicode-escape')

    input_msg = {
        'role': 'user',
        'content': content_input
    }

    messages.append(input_msg)
    
    while content_input.lower() != 'keluar':
        
        completion = client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            top_p=0.8,
            temperature=1.3
        )

        result = completion.choices
        for i in result:
            answer = i.message.content
            assist = {
                'role': 'assistant',
                'content': answer
            }
            messages.append(assist)
            print('Jawaban Chatbot: ', answer)

        inputs()

    if content_input.lower() == 'keluar':
        result = json.dumps(messages, indent=4)
        with open('sample.json', 'w') as output:
            output.write(result)
        quit()
    
inputs()