import subprocess

from metagpt.actions import Action
from metagpt.logs import logger


class SimpleRunCode(Action):
    def __init__(self, name="SimpleRunCode", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, code_text: str):
        result = subprocess.run(["python3", "-c", code_text], capture_output=True, text=True)
        code_result = result.stdout
        logger.info(f"{code_result=}")
        return code_result
