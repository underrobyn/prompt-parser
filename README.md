# prompt-parser
Parses .prompt files

# File Format

Example base file:
```ini
VERSION: 1
MODEL: gpt-3.5-turbo

[PROMPT]
You are "Alice", playing the role of a helpful chatbot.

The current challenge is: %CHALLENGE_NAME%
```

Example prompt file that uses a base file:
```ini
VERSION: 1
BASE: ./base.prompt
MODEL: gpt-3.5-turbo

[CHALLENGE_NAME]
Web DataDown
```
