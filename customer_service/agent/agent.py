from agents import Agent, Runner

from customer_service.agent.llm import llm_model
from customer_service.prompt import intent_recognizer_agent_pormpt
from customer_service.tools.order_tool import logistics_query, mock_refund_apply
from agents.run_context import RunContextWrapper


class DummyContext:
    def __init__(self):
        self.data = "something"


class RouteAgent:

    def route_agent(self):
        return Agent(
            name="用户意图分析师",
            instructions=intent_recognizer_agent_pormpt,
            model=llm_model()
        )

    async def plan(self, input: str):
        res = None
        result = await Runner.run(self.route_agent(), input)
        intent_result = result.final_output
        intent = intent_result.get("intent")
        if intent in ["物流查询", "退款申请"]:
            if intent == "物流查询":
                res = logistics_query(intent_result)
            elif intent == "退款申请":
                res = mock_refund_apply(intent_result)
        elif intent == "售前咨询":
            res = "暂不支持该功能"
        return {"code": 0, "msg": "", "data": res}
