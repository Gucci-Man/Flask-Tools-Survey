from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)

app.config["SECRET_KEY"] = "IAMBATMAN"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# keep track of questions
quest_length = len(satisfaction_survey.questions)
responses = []


@app.route("/")
def home_page():
    """The root page"""
    return render_template(
        "root.html",
        title=satisfaction_survey.title,
        steps=satisfaction_survey.instructions,
    )


@app.route("/questions/<int:quest_num>")
def question(quest_num):
    """Question Views"""
    question = satisfaction_survey.questions[quest_num].question
    choice1 = satisfaction_survey.questions[quest_num].choices[0].replace(" ", "_")
    choice2 = satisfaction_survey.questions[quest_num].choices[1].replace(" ", "_")
    return render_template(
        "question.html",
        question=question,
        choice1=choice1,
        choice2=choice2,
        quest_num=quest_num,
    )


@app.route("/answer/<int:quest_num>", methods=["POST"])
def answer(quest_num):
    """POST request then redirect to next question"""
    quest_num += 1
    choice = request.form.get("choice")
    responses.append(choice)
    flash(f"choice was {responses[quest_num-1]}")
    if quest_num >= quest_length:
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{quest_num}")


@app.route("/thanks")
def thanks():
    """Thank the user once they finish"""
    return render_template("thanks.html")
