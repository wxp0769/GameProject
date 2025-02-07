import re

import requests

# OpenRouter API URL
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"  # 注意这里使用了正确的 /chat/completions

# 替换为你的 OpenRouter API 密钥
API_KEY = "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"

# def interact_with_openrouter(prompts):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json",
#     }
#     model_list=['deepseek/deepseek-r1:free','sophosympatheia/rogue-rose-103b-v0.2:free','google/gemini-2.0-flash-thinking-exp:free','gryphe/mythomax-l2-13b:free',]
#
#     data = {
#         "model": model_list[0],  # 使用的模型，可以改为 "｜｜｜｜｜｜｜｜｜｜｜"
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompts}
#         ],
#         "max_tokens": 1000,
#         "temperature": 0.7,
#     }
#
#     try:
#         response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
#         if response.status_code == 200:
#             result = response.json()
#             print(result["choices"][0]["message"]["content"])
#             return result["choices"][0]["message"]["content"]
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#
#     return None
#
#
# # 测试调用
# if __name__ == "__main__":
#     prompts = ("用英文生成10个关于Sprunki Phase游戏的问题及答案，问题给Question,答案给Answer，返回列表，把每个问题及对应答案当成一个字典放到列表中")
#     response = interact_with_openrouter(prompts)
#     if response:
#         print(response)
def interact_with_openrouter(prompts):
    import json
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1:free",  # Optional
            "messages": [
                {
                    "role": "user",
                    "content": prompts
                }
            ]

        })
    )
    return response.json()
# result = interact_with_openrouter(prompts)
# print(type(result["choices"][0]["message"]))
# print(result["choices"][0]["message"]["content"])