import os
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args.user_prompt, args.verbose

def main():
    print("Hello from cloud-code!")
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key is None please add your api key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    user_prompt, verbose = parser()

    messages=[
        { "role": "system", "content": system_prompt},
        { "role": "user", "content": user_prompt },
    ]
    counter_of_i = 0
    for i in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            # max_tokens=100,   # temporarily done as temperature with max_tokens reuslts in None 
            messages = messages,
            temperature=0,
            tools=available_functions, # type: ignore
        )
    
        if response.usage is None:
            raise RuntimeError
    
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens
        message = response.choices[0].message
        messages.append(message)
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose)
                messages.append(result_message)
                if result_message == {}:
                    raise Exception("Error: Content of result is empty")    
                if verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            break
        counter_of_i = i
    if counter_of_i+1 == 20:
        print("The agent failed to produce a final respone")
        sys.exit(1)

        
if __name__ == "__main__":
    main()
