
import re
from typing import Dict, Generator, Optional
import itertools

import nltk
from selenium.webdriver.remote.webdriver import WebDriver

from autogpt.config import Config
from autogpt.llm import count_message_tokens, create_chat_completion
from autogpt.logs import logger
from autogpt.memory import get_memory

CFG = Config()


def split_text(
    text: str,
    max_length: int = CFG.browse_chunk_max_length,
    model: str = CFG.fast_llm_model,
    question: str = "",
) -> Generator[str, None, None]:
    flatened_paragraphs = re.sub(r"\s+", " ", text)
    sentences = nltk.sent_tokenize(flatened_paragraphs)

    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence)
        message_with_current_chunk = [create_message(" ".join(current_chunk), question)]

        expected_token_usage = (
            count_message_tokens(messages=message_with_current_chunk, model=model)
            + 1
        )
        if expected_token_usage > max_length:
            current_chunk.pop()
            if not current_chunk:
                raise ValueError("A sentence is too long to fit in a chunk.")
            yield " ".join(current_chunk)
            current_chunk = [sentence]

    if current_chunk:
        yield " ".join(current_chunk)


def summarize_text(
    url: str, text: str, question: str, driver: Optional[WebDriver] = None
) -> str:
    if not text:
        return "Error: No text to summarize"
    model = CFG.fast_llm_model
    text_length = len(text)
    logger.info(f"Text length: {text_length} characters")

    summaries = []
    chunks = list(split_text(
        text, max_length=CFG.browse_chunk_max_length, model=model, question=question
    ))
    scroll_ratio = 1 / len(chunks)

    for i, chunk in enumerate(chunks):
        if driver:
            scroll_to_percentage(driver, scroll_ratio * i)
        logger.info(f"Adding chunk {i + 1} / {len(chunks)} to memory")

        memory_to_add = f"Source: {url}\n" + chunk

        memory = get_memory(CFG)
        memory.add(memory_to_add)

        messages = [create_message(chunk, question)]
        tokens_for_chunk = count_message_tokens(messages, model)
        logger.info(
            f"Summarizing chunk {i + 1} / {len(chunks)} of length {len(chunk)} characters, or {tokens_for_chunk} tokens"
        )

        summary = create_chat_completion(
            model=model,
            messages=messages,
        )
        summaries.append(summary)
        logger.info(
            f"Added chunk {i + 1} summary to memory, of length {len(summary)} characters"
        )

        memory_to_add = f"Source: {url}\n" f"Content summary part#{i + 1}: {summary}"
        print("Memory to add :", memory_to_add)

        memory.add(memory_to_add)

    logger.info(f"Summarized {len(chunks)} chunks.")

    combined_summary = "\n".join(summaries)
    messages = [create_message(combined_summary, question)]
    return create_chat_completion(
        model=model,
        messages=messages,
    )


def scroll_to_percentage(driver: WebDriver, ratio: float) -> None:
    if ratio < 0 or ratio > 1:
        raise ValueError("Percentage should be between 0 and 1")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {ratio});")


def create_message(chunk: str, question: str) -> Dict[str, str]:
    return {
        "role": "user",
        "content": f'"""{chunk}""" Using the above text, answer the following'
        f' question: "{question}" -- if the question cannot be answered using the text,'
        " summarize the text.",
    }
