from wtforms import Form, validators
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import TextAreaField


class SentenceInputForm(Form):
    mode = RadioField(choices=[('human', 'Human language mode'), ['tree', 'Syntax tree mode']])
    sentence = TextAreaField("Input sentence", validators=[validators.input_required()],
                             default='Sunset painted the sky and sea in hues of orange and pink.')
