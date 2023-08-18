from flask import Flask, request, session, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "IAMBATMAN"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# keep track of questions
quest_length = len(survey.questions)
responses = []


@app.route("/")
def home_page():
    """The home page"""

    return render_template(
        "root.html",
        title=survey.title,
        steps=survey.instructions,
    )


@app.route("/begin", methods=["POST"])
def start_survey():
    """Start survey"""
    session["responses"] = []

    return redirect("/questions/0")


@app.route("/questions/<int:quest_num>")
def question(quest_num):
    """Display Questions"""

    if len(responses) != quest_num:
        # User attempts to access questions out of order
        flash(f"Invalid Question #:{quest_num}")
        return redirect(f"/questions/{len(responses)}")

    if quest_num >= quest_length:
        # User has answered all the questions
        return redirect("/thanks")

    question = survey.questions[quest_num].question
    # choice1 = survey.questions[quest_num].choices[0].replace(" ", "_")
    # choice2 = survey.questions[quest_num].choices[1].replace(" ", "_")

    choice1 = survey.questions[quest_num].choices[0]
    choice2 = survey.questions[quest_num].choices[1]
    return render_template(
        "question.html",
        question=question,
        choice1=choice1,
        choice2=choice2,
        quest_num=quest_num,
    )


@app.route("/answer/<int:quest_num>", methods=["POST"])
def answer(quest_num):
    """Save response then redirect to next question"""

    # Increment quest_num to go to next question
    quest_num += 1
    choice = request.form.get("choice")
    responses.append(choice)

    # save response to session
    session_responses = session["responses"]
    session_responses.append(choice)
    session["responses"] = session_responses

    print(session["responses"])

    flash(f"Choice was {responses[quest_num-1]}")

    if quest_num >= quest_length:
        # User has answered all the questions
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{quest_num}")


@app.route("/thanks")
def thanks():
    """Thank the user once they finish"""
    # resets the responses to empty list if user wish to answer survey again
    responses = []
    return render_template("thanks.html")
