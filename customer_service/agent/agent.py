from agents import Agent,Runner

from customer_service.agent.llm import llm_model
from customer_service.prompt import intent_recognizer_agent_pormpt
from customer_service.tools.order_tool import logistics_query, mock_refund_apply
from agents.run_context import RunContextWrapper


class DummyContext:
    def __init__(self):
        self.data = "something"
class RouteAgent(Agent):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def route_agent(self):
        return Agent(
            name="用户意图分析师",
            instructions=intent_recognizer_agent_pormpt,
            model=llm_model(),
            tools=[
                logistics_query,
                mock_refund_apply
            ]
        )


    async def plan(self, input: str, history: list):
        result = await Runner.run(self.route_agent(), input)
        intent_result = result.final_output
        intent = intent_result.get("intent")
        slots = intent_result.get("slots", {})

        if intent == "查询物流":
            tool = logistics_query
            output = await tool.on_invoke_tool(ctx_wrapper(), "")
        elif intent == "退货申请":
            return self.run_tool("refund_request", intent_result)
        else:
            return "抱歉，我暂时无法理解您的请求。可以重新描述一下吗？"