import enum


class Status(str, enum.Enum):
    NEW = 'NEW'
    REGISTERED = 'REGISTERED'
    CANDIDATE = 'CANDIDATE'


class LearningBackground(str, enum.Enum):
    abroad = 'abroad'
    college = 'college'
    language_school = 'languageSchool'
    never = 'never'
    self_learning = 'selfLearning'
    school = 'school'
    tutor = 'tutor'


class SkillToImprove(str, enum.Enum):
    abroad = 'differentSituationsSpeaking'
    grammar = 'grammar'
    interesting_facts = 'interestingFacts'
    pronunciation = 'pronunciation'
    reading = 'reading'
    understand_native_speakers = 'understandNativeSpeakers'
    vocabulary = 'vocabulary'


class CefrLevelExtended(str, enum.Enum):
    A1_1 = 'A1_1'
    A1_2 = 'A1_2'
    A2_1 = 'A2_1'
    A2_2 = 'A2_2'
    B1_1 = 'B1_1'
    B1_2 = 'B1_2'
    B2_1 = 'B2_1'
    B2_2 = 'B2_2'
    C1_1 = 'C1_1'
    C1_2 = 'C1_2'
    C2_1 = 'C2_1'
    C2_2 = 'C2_2'

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        return self > other or self == other

    @classmethod
    def next(cls, current):
        members = list(cls)
        index = members.index(current)
        if index < len(members) - 1:
            return members[index + 1]
        return None


class GoalToImprove(str, enum.Enum):
    mistakes = 'mistakes'
    pronunciation = 'pronunciation'
    words = 'words'
    situations = 'situations'
    barrier = 'barrier'


class GoalToLearn(str, enum.Enum):
    career = 'career'
    communication = 'communication'
    education = 'education'
    living_abroad = 'livingAbroad'
    media = 'media'
    personal_development = 'personalDevelopment'
    travel = 'travel'


class PreferredAvatarAccent(str, enum.Enum):
    american = 'american'
    british = 'british'
    indian = 'indian'
    asian = 'asian'
    australian = 'australian'
    empty = ''  # FIXME ST-1460
