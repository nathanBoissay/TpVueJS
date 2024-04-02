from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def mkpath(p):
    import os
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), p)
    )

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('./db.sqlite'))

db = SQLAlchemy(app)


 # Ensure FOREIGN KEY for sqlite3
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        

from .app import app, db
from .models import Questionnaire, Question, QuestionMultiple, QuestionSimple
with app.app_context():
    db.drop_all()
    print("Dropped the database.")
    db.create_all()
    print("Initialized the database.")
    
    questionnaire1 = Questionnaire("Questionnaire Trackamania")
    questionnaire2 = Questionnaire("Questionnaire Tensei Shittara Slime Datta Ken")
    questionnaire3 = Questionnaire("Questionnaire One Piece")
    questionnaire4 = Questionnaire("Questionnaire Solo Leveling")
    db.session.add(questionnaire1)
    db.session.add(questionnaire2)
    db.session.add(questionnaire3)
    db.session.add(questionnaire4)
    db.session.commit()
    print("Initialized the questionnaires.")


    question1 = QuestionSimple("Quelle est la meilleure voiture dans Trackmania ?", "question_simple", questionnaire1.id, "CanyonCar", "StadiumCar")
    question2 = QuestionSimple("Quelle est la durée d'un tour sur la piste Nadeo dans Trackmania ?", "question_simple", questionnaire1.id, "1 minute", "2 minutes")
    question3 = QuestionSimple("Quelle est la touche pour activer le turbo dans Trackmania ?", "question_simple", questionnaire1.id, "Shift", "Space")
    
    db.session.add(question1)
    db.session.add(question2)
    db.session.add(question3)
    db.session.commit()
    
    question4 = QuestionSimple("Quel est le nom du protagoniste de Tensei Shittara Slime Datta Ken ?", "question_simple", questionnaire2.id, "Rimuru Tempest", "Shizue Izawa")
    question5 = QuestionSimple("Quel est le nom de la ville fondée par Rimuru dans Tensei Shittara Slime Datta Ken ?", "question_simple", questionnaire2.id, "Tempest", "Milim")
    question6 = QuestionSimple("Quel est le nom de la compétence unique de Rimuru dans Tensei Shittara Slime Datta Ken ?", "question_simple", questionnaire2.id, "Great Sage", "Predator")

    db.session.add(question4)
    db.session.add(question5)
    db.session.add(question6)
    db.session.commit()
    
    question7 = QuestionMultiple("Quel est le nom du protagoniste de One Piece ?", "question_multiple", questionnaire3.id, "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp")
    question8 = QuestionMultiple("Quel est le nom du bateau de Luffy dans One Piece ?", "question_multiple", questionnaire3.id, "Going Merry", "Thousand Sunny", "Red Force", "Baratie")
    question9 = QuestionMultiple("Quel est le fruit du démon de Luffy dans One Piece ?", "question_multiple", questionnaire3.id, "Gomu Gomu no Mi", "Mera Mera no Mi", "Hito Hito no Mi", "Bara Bara no Mi")
    
    db.session.add(question7)
    db.session.add(question8)
    db.session.add(question9)
    db.session.commit()
    
    question10 = QuestionMultiple("Quel est le nom du protagoniste de Solo Leveling ?", "question_multiple", questionnaire4.id, "Sung Jin-Woo", "Cha Hae-In", "Go Gun-Hee", "Yoo Jin-Ho")
    question11 = QuestionMultiple("Quel est le nom de la guilde de Sung Jin-Woo dans Solo Leveling ?", "question_multiple", questionnaire4.id, "Hunters", "Red Gate", "White Tiger", "Black Raven")
    question12 = QuestionMultiple("Quel est le rang de Cha Hae-In dans Solo Leveling ?", "question_multiple", questionnaire4.id, "S", "A", "B", "C")
    
    db.session.add(question10)
    db.session.add(question11)
    db.session.add(question12)
    db.session.commit()

    print("Initialized the questions.")
