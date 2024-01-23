import asyncio

from tutorial_assistant import TutorialAssistant

from metagpt.logs import logger


async def main():
    msg = "Git 教程"
    role = TutorialAssistant()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)


asyncio.run(main())
