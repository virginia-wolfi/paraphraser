from wtforms import Form, validators
from wtforms.fields.simple import TextAreaField


class SentenceInputForm(Form):
    sentence = TextAreaField("Input sentence", validators=[validators.input_required()])
