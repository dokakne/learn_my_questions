from fastapi import FastAPI, Form, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import db, auth

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="html"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/", response_class=HTMLResponse)
def get_root():
    return RedirectResponse("/questions")


@app.get("/login", response_class=HTMLResponse)
def get_login():
    return templates.TemplateResponse("login.html", {"request": {}})


def get_cookied_response(email: str, password: str):
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="email", value=auth.get_jwt_token_from_email(email))
    return response


def get_retry_login_response():
    return RedirectResponse("/login?error=True", status_code=status.HTTP_302_FOUND)


@app.post("/login")
def post_login(
    email: str = Form(...), password: str = Form(...), name: str = Form(...)
):
    return (
        get_cookied_response(email, password)
        if auth.is_valid_user(
            db.User(
                id=-1,
                email=email,
                password=password,
                name=name,
            )
        )
        else get_retry_login_response()
    )


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


def get_current_user(token: str = Depends(oauth2_scheme)):
    return db.get_user_from_email(auth.get_email_from_jwt_token(token)).copy(
        update={"password": ""}
    )


@app.get("/user")
def get_user(user=Depends(get_current_user)):
    return {"user": user}


@app.post("/answer")
def post_answer(answer: db.Answer):
    db.set_answer(answer)


@app.post("/question")
def post_answer(question: db.Question):
    db.set_question(question)
