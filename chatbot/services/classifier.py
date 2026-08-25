from services.llm_service import ask_gemini, ask_gemini_fast
from services.prompts import CATEGORIES, CLASSIFY_PROMPT_TEMPLATE, FOLLOWUP_PROMPT_TEMPLATE


def _format_history(history: list[dict]) -> str:
    return "\n".join(
        f"{h.get('senderType')}: {h.get('content')}" for h in history
    ) or "(이전 대화 없음)"


async def classify(message: str, history: list[dict]) -> str:
    prompt = CLASSIFY_PROMPT_TEMPLATE.format(history=_format_history(history), message=message)
    result = (await ask_gemini_fast(prompt)).strip()

    if result not in CATEGORIES:
        return "OTHER"

    return result


async def generate_followup_reply(context: str, fixed_message: str, message: str, history: list[dict]) -> str:
    prompt = FOLLOWUP_PROMPT_TEMPLATE.format(
        context=context, fixed_message=fixed_message, history=_format_history(history), message=message
    )
    return (await ask_gemini(prompt)).strip()