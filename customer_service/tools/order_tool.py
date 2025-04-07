from agents import function_tool



def logistics_query(intent_result: dict) -> str:
    """
    调用查询物流信息的接口
    """
    if isinstance(intent_result, dict):
        order_id = intent_result.get("order_id")
        return f"订单{order_id}的物流信息是：。。。。"
    return "intent_result must be dict"

def mock_refund_apply(intent_result: dict) -> str:
    """
    退货
    """
    if isinstance(intent_result, dict):
        order_id = intent_result.get("order_id")
        return f"订单{order_id}的退款申请已提交，请耐心等待。"
    return "intent_result must be dict"