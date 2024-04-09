from metagpt.actions import UserRequirement
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from metagpt.utils.common import any_to_str
from write_crawler_code import WriteCrawlerCode
from parse_sub_requirement import ParseSubRequirement
from run_subscription import RunSubscription

# 定义订阅助手角色


class SubscriptionAssistant(Role):
    """Analyze user subscription requirements."""

    name: str = "Grace"
    profile: str = "Subscription Assistant"
    goal: str = "analyze user subscription requirements to provide personalized subscription services."
    constraints: str = "utilize the same language as the User Requirement"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._init_actions([ParseSubRequirement, RunSubscription])
        self._watch([UserRequirement, WriteCrawlerCode])

    async def _think(self) -> bool:
        cause_by = self._rc.history[-1].cause_by
        if cause_by == any_to_str(UserRequirement):
            state = 0
        elif cause_by == any_to_str(WriteCrawlerCode):
            state = 1

        if self._rc.state == state:
            self._rc.todo = None
            return False
        self._set_state(state)
        return True

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        response = await self._rc.todo.run(self._rc.history)
        msg = Message(
            content=response.content,
            instruct_content=response.instruct_content,
            role=self.profile,
            cause_by=self._rc.todo,
            sent_from=self,
        )
        self._rc.memory.add(msg)
        return msg
