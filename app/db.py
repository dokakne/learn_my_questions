from pydantic import BaseModel


class Question(BaseModel):
    id: int
    title: str
    detail: str
    author: str
    tags: list[str] = ()
    votes: int = 0
    answers: int = 0


class Answer(BaseModel):
    id: int
    question_id: int
    detail: str
    author: str
    votes: int = 0


MEDIUM_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
LARGE_TEXT = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
SMALL_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"

EMPTY_QUESTION = Question(id=-1, title="", detail="", author="")
EMPTY_ANSWER = Answer(id=-1, question_id=-1, detail="", author="")

SAMPLE_QUESTION = Question(
    id=0,
    title=SMALL_TEXT,
    detail=MEDIUM_TEXT,
    author="Nobody",
    votes=100,
    tags=("tag", "tag", "tag"),
    answers=100,
)
SAMPLE_ANSWER = Answer(
    id=0,
    question_id=1,
    detail=LARGE_TEXT,
    author="Nobody",
    votes=10,
)

QUESTIONS = [
    SAMPLE_QUESTION.copy(update={"id": 0}),
    SAMPLE_QUESTION.copy(update={"id": 1}),
    SAMPLE_QUESTION.copy(update={"id": 2}),
]


ANSWERS = [
    SAMPLE_ANSWER.copy(update={"id": 0, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 1, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 2, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 3, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 4, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 5, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 6, "question_id": 0}),
    SAMPLE_ANSWER.copy(update={"id": 7, "question_id": 1}),
    SAMPLE_ANSWER.copy(update={"id": 8, "question_id": 1}),
    SAMPLE_ANSWER.copy(update={"id": 9, "question_id": 1}),
]


def get_questions() -> list[Question]:
    return QUESTIONS


def get_question(id: int) -> Question:
    return next(
        (question for question in QUESTIONS if question.id == id), EMPTY_QUESTION
    )


def get_answers(question_id: int) -> list[Answer]:
    return (answer for answer in ANSWERS if answer.question_id == question_id)


def set_question_vote(id: int, value: int) -> None:
    get_question(id).votes += value


def get_answer(id: int) -> Answer:
    return next((answer for answer in ANSWERS if answer.id == id), EMPTY_ANSWER)


def set_answer_vote(id: int, value: int) -> None:
    get_answer(id).votes += value
