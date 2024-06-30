import os
from utils.aoai_handler import AOAIHandler
from utils.token_counter import TokenCounter
from classes.msmarkdown.msmarkdown import MSMarkdown

def msdoc_tokenizer(markdowm: MSMarkdown):
    pass

def summarize(markdown: MSMarkdown):

    # Initialize the Azure OpenAI handler
    aoai_handler = AOAIHandler()
    # Initialize the TokenCounter
    token_counter = TokenCounter()

    return markdown