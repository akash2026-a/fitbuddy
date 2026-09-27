from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .config import settings

from .database import (
    get_db,
    save_user,
    save_plan,
    get_user,
    get_latest_plan,
    update_plan,
    get_all_users,
    delete_user,
)

from .schemas import (
    UserInput,
    FeedbackRequest,
)

from .ai.gemini_generator import (
    generate_workout_gemini,
)

from .ai.gemini_flash_generator import (
    generate_nutrition_tip_with_flash,
)

from .ai.updated_plan import (
    update_workout_plan,
)


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)


def render(
    request: Request,
    template_name: str,
    **context
):
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=context,
    )


# =========================================================
# HOME PAGE
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return render(
        request,
        "index.html"
    )


# =========================================================
# GENERATE WORKOUT
# =========================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db),
):

    form_data = {
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
    }

    try:

        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

    except Exception as exc:

        return render(
            request,
            "index.html",
            error=str(exc),
            form_data=form_data,
        )

    # Save user information.
    user = save_user(
        db,
        data
    )

    # Generate the 7-day workout.
    workout_plan = generate_workout_gemini(
        username=data.username,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity,
    )

    # Generate nutrition/recovery advice.
    nutrition_tip = generate_nutrition_tip_with_flash(
        data.goal
    )

    # Save the generated plan.
    plan = save_plan(
        db,
        user,
        workout_plan,
        nutrition_tip,
    )

    return render(
        request,
        "result.html",
        user=user,
        plan=plan,
        current_plan=plan.original_plan,
        message=None,
    )


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db),
):

    try:

        request_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback,
        )

    except Exception as exc:

        return render(
            request,
            "index.html",
            error=str(exc),
        )

    # Find user.
    user = get_user(
        db,
        request_data.user_id
    )

    # Find latest plan.
    plan = get_latest_plan(
        db,
        request_data.user_id
    )

    if not user or not plan:

        return render(
            request,
            "index.html",
            error=(
                "User ID was not found. "
                "Please generate a plan first."
            ),
        )

    # Use the most recent plan as the starting point.
    base_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    # Ask Gemini to revise the plan.
    revised_plan = update_workout_plan(
        original_plan=base_plan,
        feedback=request_data.feedback,
        goal=user.goal,
        intensity=user.intensity,
    )

    # Save updated plan.
    update_plan(
        db,
        plan,
        revised_plan,
        request_data.feedback,
    )

    return render(
        request,
        "result.html",
        user=user,
        plan=plan,
        current_plan=revised_plan,
        message=(
            "Your workout plan was updated "
            "using your feedback."
        ),
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request,

    token: str | None = None,

    db: Session = Depends(get_db),
):

    # Check admin token.
    if token != settings.admin_token:

        return render(
            request,
            "admin_login.html",
        )

    # Get all users.
    users = get_all_users(db)

    return render(
        request,
        "all_users.html",
        users=users,
        token=token,
    )


# =========================================================
# DELETE USER
# =========================================================

@router.post(
    "/admin/delete/{user_id}"
)
def admin_delete_user(
    user_id: str,

    token: str = Form(...),

    db: Session = Depends(get_db),
):

    # Verify admin token.
    if token != settings.admin_token:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin token",
        )

    delete_user(
        db,
        user_id
    )

    return RedirectResponse(
        url=f"/view-all-users?token={token}",
        status_code=303,
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/api/health")
def health():

    return {
        "status": "ok",
        "app": settings.app_name,
    }