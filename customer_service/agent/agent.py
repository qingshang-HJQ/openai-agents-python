from agents import Agent


class RouteAgent(Agent):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def route_agent(self):
        return Agent(
            name="用户意图分析师",
            description=intent_recognizer_agent_pormpt,
            llm=llm_model(),
        )

    async  def plan(self, input: str, history: list):
        intent = detect_user_intent(input)
