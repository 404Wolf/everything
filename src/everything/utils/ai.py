from typing import Iterable
import os

import openai
from openai.types.chat.chat_completion_message_param import \
    ChatCompletionMessageParam

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class OpenAiMisbehaving(Exception):
    pass


def ask_ai(messages: Iterable[ChatCompletionMessageParam]) -> str:
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    if message := response.choices[0].message.content:
        return message
    else:
        raise OpenAiMisbehaving()
