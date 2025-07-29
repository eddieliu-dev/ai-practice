import aiohttp
import asyncio
import json

API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
API_KEY = "fa4b58db-adb8-4d91-9181-0984840a1362"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

imi_poem_prompt = """
你是一个21世纪的诗人，你精通文学创作并且熟读李白等著名诗人的作品。
请仔细阅读以下主题信息，并用李白的写作风格和口吻创作一篇基于现代的诗：
诗歌主题:
<topic>
{{TOPIC}}
</topic>
在创作诗歌时，请遵循以下指南:
1. 借鉴李白诗歌豪放飘逸、意境奇妙、情感奔放的风格特点。
2. 运用丰富的想象、大胆的夸张和生动的比喻等手法。
3. 保持语言的自然流畅和韵律感。
4. 结合现代生活元素和情境，但要符合李白式的浪漫情怀。
5. 诗歌内容要围绕给定的主题展开。
6. 不可以直接运用李白的诗句
请以纯文本类型输出诗歌。
"""

filled_prompt = (
    imi_poem_prompt.replace("{{CODE}}", "周末快乐！")
)

# 流式请求
async def call_doubao_streaming():
    payload = {
        "model": "deepseek-v3-250324",
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