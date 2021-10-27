import sqlite3
from .db import (
    Answer,
    Question,
    User,
    ANSWERS,
    QUESTIONS,
    EMPTY_ANSWER,
    EMPTY_QUESTION,
    EMPTY_USER,
)

DB = sqlite3.connect("data/app.db", check_same_thread=False)


def set_initialize():
    DB.execute(
        "CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY, EMAIL STRING, PASSWORD STRING, NAME STRING);"
    )
    DB.execute(
        "CREATE TABLE IF NOT EXISTS ANSWERS (ID INTEGER PRIMARY KEY, QUESTION_ID INTEGER, DETAIL STRING, AUTHOR STRING, VOTES INTEGER);"
    )
    DB.execute(
        "CREATE TABLE IF NOT EXISTS QUESTIONS (ID INTEGER PRIMARY KEY, TITLE STRING, DETAIL STRING, AUTHOR STRING, TAGS STRING, VOTES INTEGER, ANSWERS INTEGER);"
    )


def set_insert_answer(answer: Answer) -> None:
    DB.execute(
        "INSERT INTO ANSWERS(QUESTION_ID, DETAIL, AUTHOR, VOTES) VALUES(?,?,?,?)",
        (
            answer.question_id,
            answer.detail,
            answer.author,
            answer.votes,
        ),
    )
    DB.commit()


def set_insert_question(question: Question) -> None:
    DB.execute(
        "INSERT INTO QUESTIONS(TITLE, DETAIL, AUTHOR, TAGS, VOTES, ANSWERS) VALUES(?,?,?,?,?,?)",
        (
            question.title,
            question.detail,
            question.author,
            ",".join(question.tags),
            question.votes,
            question.answers,
        ),
    )
    DB.commit()


def set_insert_user(user: User) -> None:
    DB.execute(
        "INSERT INTO USERS(EMAIL, PASSWORD, NAME) VALUES(?,?,?)",
        (
            user.email,
            user.password,
            user.name,
        ),
    )
    DB.commit()


def set_add_sample_data():
    for table in ["QUESTIONS", "ANSWERS", "USERS"]:
        DB.execute(f"DELETE FROM {table};")
    DB.commit()

    for question in QUESTIONS:
        set_insert_question(question)

    for answer in ANSWERS:
        set_insert_answer(answer)


def get_question_object(question: tuple) -> Question:
    return Question(
        id=question[0],
        title=question[1],
        detail=question[2],
        author=question[3],
        tags=question[4].split(","),
        votes=question[5],
        answers=question[6],
    )


def get_answer_object(answer: tuple) -> Answer:
    return Answer(
        id=answer[0],
        question_id=answer[1],
        detail=answer[2],
        author=answer[3],
        votes=answer[4],
    )


def get_user_object(user: tuple) -> User:
    return User(id=user[0], email=user[1], password=user[2], name=user[3])


def get_questions(search: str) -> list[Question]:
    return map(
        get_question_object,
        DB.execute(f"SELECT * FROM QUESTIONS WHERE TITLE LIKE '%{search}%'").fetchall(),
    )


def get_question(id: int) -> Question:
    return next(
        map(
            get_question_object,
            DB.execute(f"SELECT * FROM QUESTIONS WHERE ID={id}").fetchall(),
        ),
        EMPTY_QUESTION,
    )


def get_answers(question_id: int) -> list[Answer]:
    return map(
        get_answer_object,
        DB.execute(f"SELECT * FROM ANSWERS WHERE QUESTION_ID={question_id}").fetchall(),
    )


def set_question_vote(id: int, value: int) -> None:
    DB.execute(f"UPDATE QUESTIONS SET VOTES = VOTES + {value} WHERE ID={id}")
    DB.commit()


def set_increment_question_answers(id: int, value: int) -> None:
    DB.execute(f"UPDATE QUESTIONS SET ANSWERS = ANSWERS + {value} WHERE ID={id}")
    DB.commit()


def get_answer(id: int) -> Answer:
    return next(
        map(get_answer_object, DB.execute(f"SELECT * FROM ANSWERS WHERE ID={id}")),
        EMPTY_ANSWER,
    )


def set_answer(answer: Answer) -> None:
    set_insert_answer(answer)
    set_increment_question_answers(answer.question_id, 1)


def set_question(question: Question) -> None:
    set_insert_question(question)


def set_answer_vote(id: int, value: int) -> None:
    DB.execute(f"UPDATE ANSWERS SET VOTES = VOTES + {value} WHERE ID={id}")
    DB.commit()


def set_user(user: User):
    set_insert_user(user)


def get_user_from_email(email: str) -> User:
    print(email)
    return next(
        map(
            get_user_object,
            DB.execute(f"SELECT * FROM USERS WHERE EMAIL='{email}'").fetchall(),
        ),
        EMPTY_USER,
    )


set_initialize()
