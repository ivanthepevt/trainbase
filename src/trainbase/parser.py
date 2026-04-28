import re
import yaml


SPECIAL_BLOCK_PATTERN = r"```(video|quiz|reflect)\n(.*?)```"


def parse_blocks(markdown_text: str):
    matches = list(re.finditer(SPECIAL_BLOCK_PATTERN, markdown_text, re.DOTALL))

    blocks = []
    last_end = 0

    for match in matches:
        if match.start() > last_end:
            blocks.append({
                "type": "markdown",
                "content": markdown_text[last_end:match.start()]
            })

        block_type = match.group(1)
        raw_content = match.group(2).strip()

        parsed_content = yaml.safe_load(raw_content) or {}

        blocks.append({
            "type": block_type,
            "content": parsed_content
        })

        last_end = match.end()

    if last_end < len(markdown_text):
        blocks.append({
            "type": "markdown",
            "content": markdown_text[last_end:]
        })

    return blocks
