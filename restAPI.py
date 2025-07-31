import aiohttp
import asyncio
import json

API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
API_KEY = "" # 火山引擎

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 🔸 非流式请求
# async def call_doubao_standard():
#     payload = {
#         "model": "doubao-1-5-pro-32k-250115",
#         "messages": [
#             {"role": "system", "content": "你是一个知识型AI助手"},
#             {"role": "user", "content": "介绍一下质数"}
#         ],
#         "stream": False
#     }
#
#     async with aiohttp.ClientSession() as session:
#         async with session.post(API_URL, headers=headers, json=payload) as resp:
#             resp_json = await resp.json()
#             content = resp_json["choices"][0]["message"]["content"]
#             print("\n【非流式输出】\n", content)


# 🔸 流式请求
async def call_doubao_streaming():
    payload = {
        "model": "doubao-1-5-pro-32k-250115",
        "messages": [
            {"role": "system", "content": "你是一个专业会议助手"},
            {"role": "user", "content": "请从下面的会议内容中提取时间、地点、人员和主题，输出JSON。\n市场部将于8月2日上午10点在三楼会议室举行品牌推广会议，林经理主持。市场部全员和顾问李宏伟参会。讨论2025年Q4推广方案。"}
        ],
        "stream": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            print("\n----- streaming request -----")
            async for line in resp.content:
                if line:
                    try:
                        # 豆包流式返回每行前缀是 "data: {json}"
                        line = line.decode().strip()
                        if line.startswith("data:"):
                            data = json.loads(line[len("data:"):])
                            delta = data["choices"][0]["delta"]["content"]
                            print(delta, end="", flush=True)
                    except Exception as e:
                        print(f"\n解析异常：{e}")
            print()

# 🔸 主运行入口
async def main():
    # await call_doubao_standard()
    await call_doubao_streaming()

if __name__ == "__main__":
    asyncio.run(main())