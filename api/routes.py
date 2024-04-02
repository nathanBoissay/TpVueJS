from flask import jsonify, abort, make_response, request, url_for
from .app import app, db
from .models import Questionnaire, Question, QuestionSimple, QuestionMultiple

@app.route("/questions", methods=["GET"])
def get_questions():
    questions = db.session.query(Question).all()
    return jsonify(questions=[q.to_json() for q in questions])

@app.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = db.session.query(Question).get(question_id)
    if question is None:
        abort(404)
    return jsonify(question.to_json())

@app.route("/questions", methods=["POST"])
def create_question():
    if not request.json or not "title" in request.json or not "type" in request.json:
        abort(400)
    if not "questionnaire_id" in request.json:
        abort(400)

    if not Questionnaire.questionnaire_existe(Questionnaire, request.json["questionnaire_id"]):
        abort(409, "Aucun questionnaire n'existe avec cet id")

    if request.json["type"] == "question_simple":
        question = QuestionSimple(request.json["title"], request.json["type"], request.json["questionnaire_id"], request.json["first_choix"], request.json["second_choix"])
        db.session.add(question)
        db.session.commit()
    elif request.json["type"] == "question_multiple":
        question = QuestionMultiple(request.json["title"], request.json["type"], request.json["questionnaire_id"],
                                     request.json["first_choix"], request.json["second_choix"], request.json["third_choix"], request.json["fourth_choix"])
        db.session.add(question)
        db.session.commit()
    else:
        abort(409)
    return jsonify(question.to_json()), 201

@app.route("/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    question = db.session.query(Question).get(question_id)
    if question is None:
        abort(404)
    if not request.json:
        abort(400)
    if "title" in request.json and type(request.json["title"]) != str:
        abort(400)
    if "choices" in request.json and type(request.json["choices"]) is list:
        choices = request.json["choices"]
        for i, choice in enumerate(choices):
            if i == 0:
                question.first_choix = choice
            elif i == 1:
                question.second_choix = choice
            elif i == 2:
                question.third_choix = choice
            elif i == 3:
                question.fourth_choix = choice
            else:
                break
    question.title = request.json.get("title", question.title)
    db.session.commit()
    return jsonify(question.to_json())

@app.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = db.session.query(Question).get(question_id)
    if question is None:
        abort(404)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"result": True})

@app.route("/questions/questionnaire/<int:questionnaire_id>", methods=["DELETE"])
def delete_questions(questionnaire_id):
    questions = db.session.query(Question).filter(Question.questionnaire_id == questionnaire_id).all()
    if questions is None:
        abort(404)
    for question in questions:
        db.session.delete(question)
    db.session.commit()
    return jsonify({"result": True})


# -------------------------- Questionnaires --------------------------

@app.route("/questionnaires", methods=["GET"])
def get_questionnaires():
    questionnaires = db.session.query(Questionnaire).all()
    return jsonify(questionnaires=[q.to_json() for q in questionnaires])

@app.route("/questionnaires/<int:questionnaire_id>", methods=["GET"])
def get_questionnaire(questionnaire_id):
    questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    return jsonify(questionnaire.to_json())

@app.route("/questionnaires", methods=["POST"])
def create_questionnaire():
    if not request.json or not "name" in request.json:
        abort(400)
    questionnaire = Questionnaire(request.json["name"])
    db.session.add(questionnaire)
    db.session.commit()
    return jsonify(questionnaire.to_json()), 201


@app.route("/questionnaires/<int:questionnaire_id>", methods=["PUT"])
def update_questionnaire(questionnaire_id):
    questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    if "name" in request.json and type(request.json["name"]) != str:
        abort(400)
    questionnaire.name = request.json.get("name", questionnaire.name)
    db.session.commit()
    return jsonify(questionnaire.to_json())

@app.route("/questionnaires/<int:questionnaire_id>", methods=["DELETE"])
def delete_questionnaire(questionnaire_id):
    questionnaire = db.session.query(Questionnaire).get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    
    delete_questions(questionnaire_id)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({"result": True})


@app.route("/questionnaires/<int:questionnaire_id>/questions", methods=["GET"])
def get_questions_by_questionnaire(questionnaire_id):
    questions = db.session.query(Question).filter(Question.questionnaire_id == questionnaire_id).all()
    return jsonify(questions=[q.to_json() for q in questions])
