import os
import re


VERSION = '1.1.0'


class PromptError(Exception):
    pass


class PromptParser:

    _PARSER_VERSION: int = 1

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.sections = {}
        self.parent = None
        self.version = None
        self.model = None

        self.load_file()

    def load_file(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        version_line = lines[0]
        if not version_line.startswith("VERSION:"):
            raise PromptError("Prompt file must start with a version")

        self.version = float(version_line.split(" ")[1].strip())

        if int(self.version) != self._PARSER_VERSION:
            raise PromptError(f"Only version {self._PARSER_VERSION}.x files are supported")

        for i, line in enumerate(lines):
            if line.startswith("BASE:"):
                base_filepath = line.split(" ")[1].strip()
                base_filepath = os.path.join(os.path.dirname(self.filepath), base_filepath)
                self.parent = PromptParser(base_filepath)

            elif line.startswith("MODEL:"):
                model = line.split(" ")[1].strip()
                self.model = model

            elif re.match(r'\[(\w+)\]', line):
                section_name = re.findall(r'\[(\w+)\]', line)[0]
                section_content = []

                for section_line in lines[i+1:]:
                    if re.match(r'\[(\w+)\]', section_line):
                        break

                    #if section_line.strip() != '':
                    section_content.append(section_line.strip())

                content = " ".join(section_content)
                if len(section_content) == 1:
                    content = content.rstrip('\n')
                    self.sections[section_name] = content
                else:
                    self.sections[section_name] = "\n".join(section_content)

        if self.parent is None and 'PROMPT' not in self.sections:
            raise PromptError("Base prompt file must contain a 'PROMPT' section")

        if self.parent is not None and self.parent.model is not None and self.model is not None:
            if self.parent.model != self.model:
                raise PromptError("Model in the current prompt file and base file must be the same")

        if self.model is None and self.parent is not None:
            self.model = self.parent.model

        if self.model is None:
            raise PromptError("You must define a model in at least the base file")

    def get_prompt(self):
        if self.parent is None:
            if 'PROMPT' not in self.sections:
                raise PromptError("Prompt file must contain a 'PROMPT' section or have a base prompt file defined")

            prompt = self.sections['PROMPT']
        else:
            if 'PROMPT' not in self.parent.sections:
                raise PromptError("Base prompt file must contain a 'PROMPT' section")

            prompt = self.parent.sections['PROMPT']

        for key, value in self.sections.items():
            if key != 'PROMPT':
                prompt = prompt.replace(f'%{key}%', value)

        return prompt
