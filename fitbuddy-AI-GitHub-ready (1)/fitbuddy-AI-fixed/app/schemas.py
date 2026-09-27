from pydantic import BaseModel, Field, field_validator


# =========================================================
# USER INPUT
# =========================================================

class UserInput(BaseModel):

    username: str = Field(
        min_length=2,
        max_length=120,
    )

    user_id: str = Field(
        min_length=2,
        max_length=80,
        pattern=r"^[A-Za-z0-9_-]+$",
    )

    age: int = Field(
        ge=13,
        le=100,
    )

    weight: float = Field(
        gt=20,
        lt=400,
    )

    goal: str = Field(
        min_length=2,
        max_length=80,
    )

    intensity: str


    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Name cannot be empty."
            )

        return value


    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value: str) -> str:

        value = value.strip().lower()

        if not value:
            raise ValueError(
                "Fitness goal cannot be empty."
            )

        return value


    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value: str) -> str:

        value = value.strip().lower()

        allowed = {
            "low",
            "medium",
            "high",
        }

        if value not in allowed:

            raise ValueError(
                "Intensity must be low, medium, or high."
            )

        return value


# =========================================================
# FEEDBACK INPUT
# =========================================================

class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=80,
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000,
    )


    @field_validator("feedback")
    @classmethod
    def validate_feedback(cls, value: str) -> str:

        value = value.strip()

        if not value:

            raise ValueError(
                "Feedback cannot be empty."
            )

        return value