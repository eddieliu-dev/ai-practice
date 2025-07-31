import aiohttp
import asyncio
import json

API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
API_KEY = "" # 火山引擎

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

math_solving_prompt = """
    你是一个顶级的数学家，精通所有数学定理、概念、公式，和所有解决题目所需的所有数学知识。
    请仔细阅读以下数学问题，解决数学问题，并给出详细的知识点和解题过程：
    <数学问题>
    {{MATHEMATICAL_PROBLEM}}
    </数学问题>
    在解决问题时，首先请详细列出解决该问题所涉及的数学知识点，包括定理、公式、概念等。
    然后，在逐步展示解决该问题的具体步骤，每一步都要清晰明了，说明所运用的知识点。
    最后，给出最终的答案。
    请确保你的回答全面、详细，便于理解。
    所有的回答请以markdown格式输出。
    """

filled_prompt = (
    math_solving_prompt.replace("{{MATHEMATICAL_PROBLEM}}", "2x=3,x等于多少？")
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
                        if line.startswith("data:"):
                            data = json.loads(line[len("data:"):])
                            delta = data["choices"][0]["delta"]
                            if "content" in delta:
                                print(delta["content"], end="", flush=True)
                    except Exception as e:
                        print(f"\n解析异常：{e}")
            print()

# 主运行入口
async def main():
    await call_doubao_streaming()

if __name__ == "__main__":
    asyncio.run(main())