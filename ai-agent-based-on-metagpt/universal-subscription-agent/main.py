import asyncio
from metagpt.team import Team
from subscription_assistant import SubscriptionAssistant
from crawler_engineer import CrawlerEngineer


if __name__ == "__main__":
    team = Team()
    team.hire([SubscriptionAssistant(), CrawlerEngineer()])
    team.run_project("从36kr创投平台 https://pitchhub.36kr.com/financing-flash爬取所有初创企业融资的信息，获取标题，链接， 时间，总结今天的融资新闻，然后在15:10发送给我")
    asyncio.run(team.run())
