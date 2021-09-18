from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from . import db

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="html"), name="static")


@app.get("/", response_class=HTMLResponse)
def get_root():
    return RedirectResponse("/questions")


@app.get("/questions", response_class=HTMLResponse)
def get_questions(search: str = ""):
    return templates.TemplateResponse(
        "questions.html", {"request": {}, "questions": db.get_questions(search)}
    )


@app.get("/question/{id}", response_class=HTMLResponse)
def get_question(id: int):
    return templates.TemplateResponse(
        "question.html",
        {
            "request": {},
            "question": db.get_question(id),
            "answers": db.get_answers(question_id=id),
        },
    )


@app.get("/qvote/{id}/{value}")
def get_question_vote(id: int, value: int):
    db.set_question_vote(id, value)
    return db.get_question(id).votes


@app.get("/avote/{id}/{value}")
def get_answer_vote(id: int, value: int):
    db.set_answer_vote(id, value)
    return db.get_answer(id).votes


@app.post("/answer")
def post_answer(answer: db.Answer):
    db.set_answer(answer)


@app.post("/question")
def post_answer(question: db.Question):
    db.set_question(question)
