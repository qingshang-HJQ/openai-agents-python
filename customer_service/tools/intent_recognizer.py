from agents import Agent
from customer_service.agent.llm import llm_model
from customer_service.prompt import intent_recognizer_agent_pormpt


# noinspection PyArgumentList
def intent_recognizer_agent():
    return Agent(
        name="用户意图分析师",
        description=intent_recognizer_agent_pormpt,
        llm=llm_model(),
    )

