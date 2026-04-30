from . import db

class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Response to Question {self.question_id}: {"Agree" if self.is_agree else "Disagree"}>'