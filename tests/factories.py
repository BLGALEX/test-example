import factory
from factory import fuzzy
import random
from uuid import uuid4

from src.api.models.user import User
from src.api.enums import (
    Status,
    LearningBackground,
    SkillToImprove,
    CefrLevelExtended,
    GoalToImprove,
    GoalToLearn,
    PreferredAvatarAccent,
)


INTERESTS = [f"interest_{i}" for i in range(10)]
SITUATIONS = [f"situation_{i}" for i in range(10)]
DESIRED_OUTCOMES = [f"outcome_{i}" for i in range(10)]


def generate_timezone():
    hours = random.randint(0, 23)
    minutes = random.choice([0, 30])
    sign = random.choice(['+', '-'])
    timezone_str = f"{sign}{hours:02d}:{minutes:02d}"
    return timezone_str


def custom_phone_number_generator():
    return '+' + ''.join([str(random.randint(0, 9)) for _ in range(random.randint(10, 15))])


class UserModelFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(lambda: str(uuid4()))
    goal_to_learn = GoalToLearn.career
    interests = factory.LazyFunction(lambda: random.sample(INTERESTS, 3))
    name = factory.Sequence(lambda n: f"name_{n}")
    email = factory.Faker("email")
    status = Status.NEW.value
    language = factory.Faker("language_code")
    goals_to_improve = [GoalToImprove.barrier, GoalToImprove.pronunciation]
    daily_goal = factory.Faker("word")
    level = factory.Faker("word")
    situations = factory.LazyFunction(lambda: random.sample(SITUATIONS, 3))
    preferred_accent = PreferredAvatarAccent.american
    gender = fuzzy.FuzzyChoice(["male", "female", "other"])
    age = factory.LazyFunction(lambda: str(random.randint(18, 100)))
    selected_course_id = factory.LazyFunction(lambda: str(uuid4()))
    desired_outcomes = factory.LazyFunction(lambda: random.sample(DESIRED_OUTCOMES, 3))
    learning_pleasure = factory.Faker("word")
    skill_to_improve = SkillToImprove.grammar
    fcm_token = factory.Faker("pystr", min_chars=10, max_chars=20)
    timezone = factory.LazyFunction(generate_timezone)
    learning_background = [LearningBackground.abroad, LearningBackground.school]
    is_onboarding_lesson_screen_passed = factory.Faker("boolean")
    is_personal_plan_screen_passed = factory.Faker("boolean")
    timer_time_mins = factory.Faker("pyint", min_value=5, max_value=60)
    timer_reset_interval_mins = factory.Faker("pyint", min_value=60, max_value=360)
    default_avatar_id = factory.LazyFunction(lambda: str(uuid4()))
    cefr_level_extended = CefrLevelExtended.A1_1.value
