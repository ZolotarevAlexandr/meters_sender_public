from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class CountersForm(FlaskForm):
    kitchen_hot = IntegerField('Кухня, горячая вода', validators=[DataRequired()])
    kitchen_cold = IntegerField('Кухня, холодная вода', validators=[DataRequired()])
    bathroom_hot = IntegerField('Ванная, горячая вода', validators=[DataRequired()])
    bathroom_cold = IntegerField('Ванная, холодная вода', validators=[DataRequired()])
    electricity = IntegerField('Электричество', validators=[DataRequired()])
    submit = SubmitField('Отправить')
