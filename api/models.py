from .app import db

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Questionnaire %r>' % self.name
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [question.to_json() for question in self.questions]
        }
    

    def questionnaire_existe(self, id_questionnaire):
        return Questionnaire.query.filter_by(id=id_questionnaire).first()
    

    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    title = db.Column(db.String(200))
    type = db.Column(db.String(50))

    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship('Questionnaire',backref=db.backref('questions', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'with_polymorphic':'*',
        'polymorphic_on': 'type'
    }

    def __init__(self, title, type, questionnaire_id):
        self.title = title
        self.type = type
        self.questionnaire_id = questionnaire_id


    def __repr__(self):
        return '<Question %r>' % self.title
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'questionnaire_id': self.questionnaire_id
        }


class QuestionSimple(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    first_choix = db.Column(db.String(200))
    second_choix = db.Column(db.String(200))

    __mapper_args__ = {
        'polymorphic_identity':'question_simple',
        'with_polymorphic':'*',
        'polymorphic_load': 'inline'
    }

    def __init__(self, title, type, questionnaire_id, first_choix, second_choix):
        super().__init__(title, type, questionnaire_id)
        self.first_choix = first_choix
        self.second_choix = second_choix
    
    def to_json(self):
        json = super().to_json()
        json.update({'first_choix': self.first_choix,'second_choix':self.second_choix})
        return json
    
class QuestionMultiple(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    first_choix = db.Column(db.String(200))
    second_choix = db.Column(db.String(200))
    third_choix = db.Column(db.String(200))
    fourth_choix = db.Column(db.String(200))

    __mapper_args__ = {
        'polymorphic_identity':'question_multiple',
        'with_polymorphic':'*',
        'polymorphic_load': 'inline'
    }

    def __init__(self, title, type, questionnaire_id, first_choix, second_choix, third_choix, fourth_choix):
        super().__init__(title, type, questionnaire_id)
        self.first_choix = first_choix
        self.second_choix = second_choix
        self.third_choix = third_choix
        self.fourth_choix = fourth_choix
     
    def to_json(self):
        json = super().to_json()
        json.update({'first_choix': self.first_choix,'second_choix':self.second_choix,
            'third_choix':self.third_choix,'fourth_choix':self.fourth_choix})
        return json