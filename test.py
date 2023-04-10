from src.PromptFileParser import PromptParser, PromptError


if __name__ == '__main__':
    try:
        parser = PromptParser("prompts/web_datadown.prompt")
        print(parser.get_prompt())
    except PromptError as e:
        print(e)
