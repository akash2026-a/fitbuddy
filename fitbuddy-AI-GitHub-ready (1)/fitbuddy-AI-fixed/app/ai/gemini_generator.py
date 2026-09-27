from .gemini_client import generate_text

from ..config import settings


# =========================================================
# DEMO WORKOUT
# =========================================================

def demo_workout(
    goal: str,
    intensity: str,
) -> str:

    return f"""
7-DAY {goal.upper()} FITNESS PLAN

Intensity: {intensity.title()}


DAY 1 - FULL BODY

Warm-up:
7 minutes of brisk walking and light mobility.

Main Workout:
- Bodyweight squats: 3 sets x 10 reps
- Push-ups: 3 sets x 8 reps
- Rows: 3 sets x 10 reps
- Glute bridges: 3 sets x 12 reps

Cooldown:
5 minutes of easy walking and gentle stretching.


DAY 2 - CARDIO

Warm-up:
5 minutes at an easy pace.

Main Workout:
25 minutes of comfortable-to-moderate cardio.

Optional:
Use short faster periods followed by easier recovery
periods.

Cooldown:
5 minutes of easy movement.


DAY 3 - RECOVERY

Activity:
20-30 minute easy walk.

Mobility:
Gentle full-body mobility.

Focus:
Recovery and preparation for the rest of the week.


DAY 4 - FULL BODY STRENGTH

Warm-up:
7 minutes.

Main Workout:
- Reverse lunges: 3 sets x 8 reps per side
- Overhead press: 3 sets x 10 reps
- Hip hinge: 3 sets x 10 reps
- Plank: 3 sets x 20-30 seconds

Cooldown:
5-10 minutes of easy movement.


DAY 5 - CARDIO + CORE

Warm-up:
5 minutes.

Main Workout:
20-30 minutes of cardio.

Core:
- Dead bug: 3 sets x 10 per side
- Side plank: 2 sets x 20 seconds per side

Cooldown:
5 minutes.


DAY 6 - STRENGTH TECHNIQUE

Warm-up:
7 minutes.

Main Workout:
Practice the major movements from Days 1 and 4
using controlled technique.

Keep the volume manageable and prioritize good form.

Cooldown:
5-10 minutes.


DAY 7 - REST / ACTIVE RECOVERY

Take a rest day.

Optional:
Easy walking and gentle mobility as comfortable.


GENERAL GUIDANCE

Adjust exercise volume according to your experience
and recovery.

Stop exercising if you experience pain, dizziness,
or unusual symptoms.

This is general fitness information and is not
individualized medical advice.
""".strip()


# =========================================================
# GEMINI WORKOUT GENERATOR
# =========================================================

def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    prompt = f"""
Create a personalized 7-day fitness plan.

USER INFORMATION

Name:
{username}

Age:
{age}

Weight:
{weight} kg

Fitness Goal:
{goal}

Preferred Workout Intensity:
{intensity}


REQUIREMENTS

Create exactly 7 labeled days.

For every day include:

1. Day number and focus
2. Warm-up
3. Main workout
4. Exercises
5. Sets and repetitions or duration
6. Cooldown or recovery guidance

Include at least one recovery/rest day.

Keep the recommendations practical.

Do not require specialized equipment unless
it is clearly marked as optional.

Consider the user's selected goal and intensity.

Avoid medical claims.

Do not recommend training through pain.

The result should be easy for a normal user
to read and follow.
"""

    result = generate_text(
        prompt,
        settings.workout_model,
    )

    # If Gemini responds successfully,
    # return the AI-generated plan.
    if result:
        return result

    # If there is no Gemini API key or the API
    # is unavailable, use the built-in demo plan.
    return demo_workout(
        goal,
        intensity,
    )