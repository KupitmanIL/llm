from zoneinfo import reset_tzpath

from ollama import chat
import json
from tools import TOOLS
from system_content import SYSTEM_CONTENT


URL = 'http://localhost:11434/api/chat'
MODEL_NAME = 'phi3'


def chat_request(messages):
    stream = chat(model=MODEL_NAME,messages=messages, stream=True)
    full_reply = ''
    try:
        stream = chat(model=MODEL_NAME,messages=messages, stream=True)
        for chunk in stream:
            piece = chunk['message']['content']
            print(piece, end='', flush=True)
            full_reply += piece
    except Exception as e:
        print(f"Error: {e}",end='')
    print()
    return full_reply

def parse_tool_call(text):
    start,end = text.find('{'),text.rfind('}')
    if start == 1 or end == -1:
        return None
    try:
        data = json.loads(text[start:end+1])
    except json.JSONDecodeError:
        return None
    return data if isinstance(data,dict) and 'tool' in data else None

def call_tool(tool_call:dict):
    tool = TOOLS.get(tool_call.get('tool'))
    if not tool:
        return None
    return tool(tool_call.get('arguments', {}))

def main():
    messages = [
        {
            'role': 'system',
            'content': SYSTEM_CONTENT
        }
    ]
    print('phi-3 simple chat. Type "exit" to quit.')
    while True:
        user_input = input('You: ')
        if user_input == 'exit':
            print('Bye')
            break
        messages.append({
            'role': 'user',
            'content': user_input
        })
        print('\nAssistant:', end='', flush=True)
        reply = chat_request(messages)
        messages.append({
            'role': 'assistant',
            'content': reply
        })
        tool_call = call_tool(reply)
        if tool_call:
            tool_result = call_tool(tool_call)
            if tool_result:
                messages.append({
                    'role': 'system',
                    'content': f'Tool result: {tool_result}\n Answer the user`s last question using the tool result'
                })
                print('\nAssistant:', end='', flush=True)
                reply = chat_request(messages)
                messages.append({
                    'role': 'assistant',
                    'content': reply
                })
        print()
        print('_' * 60)


main()
