from simple_run_code import SimpleRunCode
from simple_write_code import SimpleWriteCode

from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message


class RunnableCoder(Role):
    def __init__(
        self,
        name: str = "Alice",
        profile: str = "RunnableCoder",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([SimpleWriteCode, SimpleRunCode])
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: 准备 {self._rc.todo}")
        todo = self._rc.todo

        msg = self.get_memories(k=1)[0]  # 得到最相似的 k 条消息
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self._rc.memory.add(msg)
        return msg
