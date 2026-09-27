from .gemini_client import generate_text

from ..config import settings


# =========================================================
# DEMO PLAN UPDATE (fallback when no API key is configured)
# =========================================================

def demo_updated_plan(original_plan: str, feedback: str) -> str:

    return (
        f"{original_plan}\n\n"
        "-----------------------------------------\n"
        "USER FEEDBACK NOTED (demo mode - no AI revision applied):\n"
        f"{feedback}\n"
        "Consider adjusting exercise volume, intensity, or exercise "
        "selection above to reflect this feedback.\n"
    )


# =========================================================
# GEMINI PLAN REVISION
# =========================================================

def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
) -> str:

    prompt = f"""
Here is a user's current 7-day fitness plan:

{original_plan}

The user's fitness goal is: {goal}
The user's preferred intensity is: {intensity}

The user has given the following feedback about the plan:

{feedback}

Revise the 7-day plan to address this feedback while keeping
the same structure (7 labeled days, each with warm-up, main
workout, exercises, sets/reps or duration, and cooldown).
Keep at least one recovery/rest day. Avoid medical claims and
do not recommend training through pain.
"""

    result = generate_text(
        prompt,
        settings.workout_model,
    )

    # If Gemini responds successfully, return the revised plan.
    if result:
        return result

    # Otherwise fall back to appending the feedback to the plan.
    return demo_updated_plan(
        original_plan,
        feedback,
    )
