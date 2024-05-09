from uuid import uuid4

from praktika_shared_lib.db import Base, Timestamped
from sqlalchemy import ARRAY, Column, Enum, String, Boolean, Integer
from sqlalchemy.dialects import postgresql as pg

from src.api.enums import Status, LearningBackground, SkillToImprove, CefrLevelExtended


class User(Base, Timestamped):
    __tablename__ = 'user'

    # common
    id = Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid4)
    goal_to_learn = Column(String())
    interests = Column(ARRAY(String()))

    # backen-api-service
    name = Column(String(1000))
    email = Column(String(1000))
    status = Column(Enum(Status, name='AccountStatus'), default=Status.NEW)
    language = Column(String(10))
    goals_to_improve = Column(ARRAY(String()))
    daily_goal = Column(String())
    level = Column(String())
    situations = Column(ARRAY(String()))
    preferred_accent = Column(String())
    gender = Column(String())
    age = Column(String())
    selected_course_id = Column(pg.UUID(as_uuid=True))
    desired_outcomes = Column(ARRAY(String()))
    learning_pleasure = Column(String())
    skill_to_improve = Column(Enum(SkillToImprove, name='SkillToImprove'))
    fcm_token = Column(String())
    timezone = Column(String())
    learning_background = Column(ARRAY(Enum(LearningBackground, name='LearningBackground')))
    is_onboarding_lesson_screen_passed = Column(Boolean())
    is_personal_plan_screen_passed = Column(Boolean())
    timer_time_mins = Column(Integer())
    timer_reset_interval_mins = Column(Integer())

    # gpt-lessons-service
    default_avatar_id = Column(pg.UUID(as_uuid=True))
    cefr_level_extended = Column(Enum(CefrLevelExtended))
