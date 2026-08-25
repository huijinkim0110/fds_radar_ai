from services.llm_service import ask_gemini, ask_gemini_fast
from services.prompts import CATEGORIES, CLASSIFY_PROMPT_TEMPLATE, FOLLOWUP_PROMPT_TEMPLATE, POLICY_QUESTION_PROMPT_TEMPLATE


def _format_history(history: list[dict]) -> str:
    return "\n".join(
        f"{h.get('senderType')}: {h.get('content')}" for h in history
    ) or "(이전 대화 없음)"


async def classify(message: str, history: list[dict]) -> tuple[str, str]:
    prompt = CLASSIFY_PROMPT_TEMPLATE.format(history=_format_history(history), message=message)
    result = (await ask_gemini_fast(prompt)).strip()

    category, _, req_type = result.partition("|")
    category = category.strip()
    req_type = req_type.strip()

    if category not in CATEGORIES:
        return "OTHER", "REQUEST"
    if req_type not in ("REQUEST", "QUESTION"):
        req_type = "REQUEST"  # 파싱 실패 시 안전하게 기존 동작(REQUEST)으로 폴백

    return category, req_type


async def generate_followup_reply(context: str, fixed_message: str, message: str, history: list[dict]) -> str:
    prompt = FOLLOWUP_PROMPT_TEMPLATE.format(
        context=context, fixed_message=fixed_message, history=_format_history(history), message=message
    )
    return (await ask_gemini(prompt)).strip()


async def generate_policy_answer(policy_fact: str, message: str, history: list[dict]) -> str:
    prompt = POLICY_QUESTION_PROMPT_TEMPLATE.format(
        policy_fact=policy_fact, history=_format_history(history), message=message
    )
    return (await ask_gemini(prompt)).strip()