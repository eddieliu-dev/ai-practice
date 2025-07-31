import aiohttp
import asyncio
import json

API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
API_KEY = "" # 火山引擎

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

code_examine_prompt = """
你是一个世界级的软件工程师，你精通所有的编程语言，软件系统和架构。
审查以下代码，并指出代码中存在错误的位置，并修改错误代码：
<代码>
{{CODE}}
</代码>
在审查代码时，请仔细检查代码的语法、逻辑和潜在的运行时错误。
请确保你的分析和错误位置的指出准确、清晰，而且保证修改过的代码不能有任何错误。
请以纯文本格式指出错误的位置。
请以结构清晰完整的markdown格式输出修改后的代码。
"""

filled_prompt = (
    code_examine_prompt.replace("{{CODE}}", "print(hello world)")
)

# 流式请求
async def call_doubao_streaming():
    payload = {
        "model": "doubao-seed-1-6-thinking-250715",
        "messages": [
            {"role": "user", "content": filled_prompt},
        ],
        "stream": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            async for line in resp.content:
                if line:
                    try:
                        # 豆包流式返回每行前缀是 "data: {json}"
                        line = line.decode().strip()
                        # if line.startswith("data:"):
                        #     data = json.loads(line[len("data:"):])
                        #     delta = data["choices"][0]["delta"]["content"]
                        #     if "content" in delta:
                        #         print(delta["content"], end="", flush=True)
                        print(line)
                    except Exception as e:
                        print(f"\n解析异常：{e}")
            print()

# 主运行入口
async def main():
    await call_doubao_streaming()

if __name__ == "__main__":
    asyncio.run(main())