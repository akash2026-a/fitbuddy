from .gemini_client import generate_text

from ..config import settings


# =========================================================
# DEMO NUTRITION TIP (fallback when no API key is configured)
# =========================================================

def demo_nutrition_tip(goal: str) -> str:

    return (
        f"NUTRITION & RECOVERY TIP FOR '{goal.upper()}'\n\n"
        "Stay hydrated throughout the day and prioritize whole, "
        "minimally processed foods. Include a source of protein "
        "with each meal, eat a mix of colorful vegetables and "
        "fruit, and get 7-9 hours of sleep to support recovery. "
        "This is general guidance, not individualized medical or "
        "dietary advice."
    )


# =========================================================
# GEMINI NUTRITION TIP GENERATOR
# =========================================================

def generate_nutrition_tip_with_flash(goal: str) -> str:

    prompt = f"""
Provide a short, practical nutrition and recovery tip
(3-5 sentences) for someone whose fitness goal is:

{goal}

Keep it general, safe, and free of medical claims.
Do not prescribe exact calorie or macro targets.
"""

    result = generate_text(
        prompt,
        settings.nutrition_model,
    )

    # If Gemini responds successfully, use it.
    if result:
        return result

    # Otherwise fall back to the built-in demo tip.
    return demo_nutrition_tip(goal)
