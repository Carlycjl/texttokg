import sys
from yachalk import chalk
sys.path.append("..")

import json
import ollama.client as client


def extractConcepts(prompt: str, metadata={}, model="mistral-openorca:latest"):
    SYS_PROMPT = (
        "你的任务是提取给定上下文中提及的关键概念（和非个人实体）。 "
        "仅提取最重要且原子化的概念，如果需要，将概念分解为更简单的概念。"
        "将概念分类为以下其中一种类别： "
        "[事件，概念，地点，物体，文档，组织，条件，其他]\n"
        "将输出格式化为以下JSON列表的格式：\n"
        "[\n"
        "   {\n"
        '       "entity": 概念，\n'
        '       "importance": 概念的上下文重要性，以1到5的等级划分（5为最高），\n'
        '       "category": 概念类型，n'
        "   }, \n"
        "{ }, \n"
        "]\n"
    )
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\n错误 ### 这是有错误的响应： ", response, "\n\n")
        result = None
    return result


def graphPrompt(input: str, metadata={}, model="mistral-openorca:latest"):
    if model == None:
        model = "mistral-openorca:latest"

    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
        "你是一个网络图制作者，从给定的上下文中提取术语及其关系。这些术语应该根据上下文代表关键概念。 "
        "你被提供了一个上下文块（用```分隔）。你的任务是提取出给定上下文中提到的术语的本体。 "
        "这些术语应该根据上下文代表关键概念。 \n"
        "思路 1：在遍历每个句子时，思考其中提到的关键术语。\n"
            "\t术语可能包括对象、实体、位置、组织、人物、条件、缩写、文件、服务、概念等。\n"
            "\t术语应尽可能原子化。\n\n"
        "思路 2：思考这些术语如何与其他术语之间建立一对一的关系。\n"
            "\t在同一句子或同一段落中提到的术语通常相互关联。\n"
            "\t术语可能与许多其他术语相关。\n\n"
        "思路 3：找出每对相关术语之间的关系。 \n\n"
        "将输出格式化为一个JSON列表。列表的每个元素包含一对术语及其之间的关系，格式如下： \n"
        "[\n"
        "   {\n"
        '       "node_1": "提取的本体论中的一个概念，一般为名词",\n'
        '       "node_2": "提取的本体论中的一个与node_1相关的概念",\n'
        '       "edge": "两个概念之间的关系，可以用一两个句子描述"\n'
        "   }, {...}\n"
        "]"
    )

    USER_PROMPT = f"上下文: ```{input}``` \n\n 输出: "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\n错误 ### 这是有错误的响应： ", response, "\n\n")
        result = None
    return result
