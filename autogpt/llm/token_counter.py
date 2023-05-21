"""Functions for counting the number of tokens in a message or string."""
from __future__ import annotations

from typing import List
from nltk.tokenize import word_tokenize
import openai
from autogpt.llm.base import Message
from autogpt.logs import logger
import re


def preprocess_text(text: str) -> str:
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Replace specific characters or sequences with placeholders
    text = re.sub(r'([^\w\s-])', r' \1 ', text)

    # Separate punctuation from words
    text = re.sub(r'(\w+)([!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~])', r'\1 \2 ', text)

    # Separate hyphens that are not part of words
    text = re.sub(r'(\s-|-\s)', r' - ', text)

    return text


def count_message_tokens(
    messages: List[Message], model: str = "gpt-3.5-turbo-0301"
) -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
        messages (list): A list of messages, each of which is a dictionary
            containing the role and content of the message.
        model (str): The name of the model to use for tokenization.
            Defaults to "gpt-3.5-turbo-0301".

    Returns:
        int: The number of tokens used by the list of messages.
    """
    if model == "gpt-3.5-turbo":
        # !Note: gpt-3.5-turbo may change over time.
        # Returning num tokens assuming gpt-3.5-turbo-0301.")
        return count_message_tokens(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # !Note: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return count_message_tokens(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows {role/name}\n{content}\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"num_tokens_from_messages() is not implemented for model {model}.\n"
            " See https://github.com/openai/openai-python/blob/main/chatml.md for"
            " information on how messages are converted to tokens."
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            preprocessed_value = preprocess_text(value)
            num_tokens += len(word_tokenize(preprocessed_value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with assistant
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The text string.
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    preprocessed_string = preprocess_text(string)
    return len(word_tokenize(preprocessed_string))
