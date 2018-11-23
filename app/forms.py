from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class EditForm (FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content")
    update = SubmitField("Update")

