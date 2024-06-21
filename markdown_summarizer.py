import os
from utils.aoai_handler import AOAIHandler
from utils.token_counter import TokenCounter
from .markdown import Markdown

def msdoc_tokenizer(markdowm: Markdown):
    pass

def summrize(markdown: Markdown):

    # Initialize the Azure OpenAI handler
    aoai_handler = AOAIHandler()
    # Initialize the TokenCounter
    token_counter = TokenCounter()

    return markdown