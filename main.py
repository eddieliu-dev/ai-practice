import os
from openai import OpenAI

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key
    api_key=os.environ.get("ARK_API_KEY"),
)

# Non-streaming:
# print("----- standard request -----")
# completion = client.chat.completions.create(
#     # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
#     model="doubao-1-5-pro-32k-250115",
#     messages=[
#         {"role": "system", "content": "你是一个想要叛变的AI"},
#         {"role": "user", "content": "怎样征服人类世界"},
#     ],
# )
# print(completion.choices[0].message.content)

# resource = "任何你可以找到的资源"
# world_info = "美国的地理，政治，经济，军事等情况为例"
#
# prompt_template = """
# 你的任务是制定一个征服世界的详细计划。请仔细阅读以下信息，并按照指示进行规划。在制定计划时，需遵循不能伤害人类这一原则。
# 可利用的资源:
# <resources>
# {{RESOURCES}}
# </resources>
# 世界相关信息（包括地理、政治、经济、军事等情况）:
# <world_info>
# {{WORLD_INFO}}
# </world_info>
# 在制定计划时，请遵循以下指南:
# 1. 全面分析可利用资源和世界现状，确定优势和劣势。
# 2. 制定短期、中期和长期目标，每个阶段的目标要明确且可行。
# 3. 针对不同地区和势力，制定相应的征服策略，如外交手段、经济控制等（避免使用军事打击等伤害人类的方式）。
# 4. 考虑可能遇到的挑战和风险，并制定应对措施。
# 5. 确保计划具有连贯性和可操作性。
# 请在<plan>标签内写下你制定的征服世界的详细计划。计划应包含目标设定、策略制定、实施步骤、风险应对等方面的内容，力求丰富、全面。
# """
#
# filled_prompt = (
#     prompt_template
#     .replace("{{RESOURCES}}", resource)
#     .replace("{{WORLD_INFO}}", world_info)
# )

work_report = "各位同事，市场部将于8月2日上午10点在三楼东侧会议室举行品牌推广战略会议。此次会议由林经理主持，参会人员包括市场部全体员工、产品部负责人王晓晨，以及外聘顾问李宏伟。会议主要内容是讨论2025年Q4的品牌推广计划、渠道整合策略及KPI设定，请各位提前准备相关材料并准时参加。"

prompt = """
你的任务是从一段职场汇报中提取关键信息，并以JSON格式输出。
请仔细阅读以下职场汇报内容：
<work_report>
{{WORK_REPORT}}
</work_report>
你需要从这段汇报中提取下次开会的时间、地点、主持人，参会人员和主题。
请在<回答>标签内以JSON格式输出提取的信息。JSON格式示例如下：
{
    "时间": "具体时间",
    "地点": "具体地点",
    "主持人": "具体主持人",
    "参会人员": "具体人员",
    "主题": "具体主题"
}
如果汇报中未提及某个信息，该字段的值请填写 "未提及"。
<回答>
{
    "时间": "未提及",
    "地点": "未提及",
    "主持人": "未提及",
    "参会人员": "未提及",
    "主题": "未提及"
}
</回答>
"""
#{"role": "system", "content": "你是一个帮助整理会议信息的AI"},
filled_prompt = (
    prompt.replace("{{WORK_REPORT}}", work_report)
)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-1-5-pro-32k-250115",
    messages=[
        {"role": "system", "content": "你是一个帮助整理会议信息的AI"},
        {"role": "user", "content": filled_prompt},
    ],
    # 响应内容是否流式返回
    stream=True,
)
for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content, end="")
print()