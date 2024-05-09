from typing import Literal
from uuid import UUID

import pycountry
from praktika_shared_lib.fastapi.schemas import CamelizeableModel
from pydantic import AnyUrl, EmailStr, Field, validator

from src.api.enums import (
    Status,
    LearningBackground,
    SkillToImprove,
    CefrLevelExtended,
    GoalToLearn,
    GoalToImprove,
    PreferredAvatarAccent,
)
from src.api.models.user import User


countries = tuple(it.alpha_2 for it in pycountry.countries)
Country = Literal[countries]


class UserBaseModel(CamelizeableModel):
    goal_to_learn: GoalToLearn | None
    interests: list[str] | None
    name: str | None = Field(None, max_length=1000)
    email: EmailStr | Literal[''] | None
    status: Status | None
    language: str | None = Field(None, max_length=10)
    goals_to_improve: list[GoalToImprove] | None
    daily_goal: str | None
    level: str | None
    situations: list[str] | None
    preferred_accent: PreferredAvatarAccent | None
    gender: str | None
    age: str | None
    selected_course_id: UUID | None
    desired_outcomes: list[str] | None
    learning_pleasure: str | None
    skill_to_improve: SkillToImprove | None
    fcm_token: str | None
    timezone: str | None = Field(None, regex=r'[\+|-][0-9]{2}:[0-9]{2}')
    learning_background: list[LearningBackground] | None
    is_onboarding_lesson_screen_passed: bool | None
    is_personal_plan_screen_passed: bool | None
    timer_time_mins: int | None
    timer_reset_interval_mins: int | None
    default_avatar_id: UUID | None
    cefr_level_extended: CefrLevelExtended | None

    @validator('email', pre=True, always=True)
    def validate_email(cls, v):
        if v is not None:
            if len(v) > 1000:
                raise ValueError('email must be less than 1000 characters')
        return v


class UserUpdateModel(UserBaseModel):
    pass


class UserCreateModel(UserBaseModel):
    id: UUID | None

    @validator('id', pre=True, always=False)
    def validate_id(cls, value):
        if value is None:
            raise ValueError('id must be not None')
        return value


class UserOutputModel(UserBaseModel):
    id: UUID
