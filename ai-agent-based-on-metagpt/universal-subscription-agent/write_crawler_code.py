import datetime
import sys
from typing import Optional
from uuid import uuid4

from aiocron import crontab
from metagpt.actions import UserRequirement
from metagpt.actions.action import Action
from metagpt.actions.action_node import ActionNode
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.tools.web_browser_engine import WebBrowserEngine
from metagpt.utils.common import CodeParser, any_to_str
from metagpt.utils.parse_html import _get_soup
from pytz import BaseTzInfo
from metagpt.logs import logger

PROMPT_TEMPLATE = """Please complete the web page crawler parse function to achieve the User Requirement. The parse \
function should take a BeautifulSoup object as input, which corresponds to the HTML outline provided in the Context.

```python
from bs4 import BeautifulSoup

# only complete the parse function
def parse(soup: BeautifulSoup):
    ...
    # Return the object that the user wants to retrieve, don't use print
```

## User Requirement
{requirement}

## Context

The outline of html page to scrabe is show like below:

```tree
{outline}
```
"""

# 辅助函数: 获取html css大纲视图


def get_outline(page):
    soup = _get_soup(page.html)
    outline = []

    def process_element(element, depth):
        name = element.name
        if not name:
            return
        if name in ["script", "style"]:
            return

        element_info = {"name": element.name, "depth": depth}

        if name in ["svg"]:
            element_info["text"] = None
            outline.append(element_info)
            return

        element_info["text"] = element.string
        # Check if the element has an "id" attribute
        if "id" in element.attrs:
            element_info["id"] = element["id"]

        if "class" in element.attrs:
            element_info["class"] = element["class"]
        outline.append(element_info)
        for child in element.children:
            process_element(child, depth + 1)

    for element in soup.body.children:
        process_element(element, 1)

    return outline


# 写爬虫代码的Action


class WriteCrawlerCode(Action):
    async def run(self, requirement):
        requirement: Message = requirement[-1]
        data = requirement.instruct_content.dict()
        urls = data["Crawler URL List"]
        query = data["Page Content Extraction"]

        codes = {}
        for url in urls:
            codes[url] = await self._write_code(url, query)
        return "\n".join(f"# {url}\n{code}" for url, code in codes.items())

    async def _write_code(self, url, query):
        page = await WebBrowserEngine().run(url)
        outline = get_outline(page)
        outline = "\n".join(
            f"{' '*i['depth']}{'.'.join([i['name'], *i.get('class', [])])}: {i['text'] if i['text'] else ''}"
            for i in outline
        )
        code_rsp = await self._aask(PROMPT_TEMPLATE.format(outline=outline, requirement=query))
        code = CodeParser.parse_code(block="", text=code_rsp)
        return code
