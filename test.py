from PromptFile import PromptParser, PromptError


if __name__ == '__main__':
    try:
        parser = PromptParser("prompts/bad.prompt")
        print(parser.get_prompt())
    except PromptError as e:
        print(e)
