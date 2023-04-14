from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class UserInfoForm(FlaskForm):
    receiver_email = StringField('Ведите e-mail получателя', validators=[DataRequired()])
    app_password = PasswordField('Введите пароль приложения', validators=[DataRequired()])
    additional_info = StringField('Введите дополнительную информацию', validators=[DataRequired()])
    name_surname = StringField('Введите имя и фамилию', validators=[DataRequired()])
    phone = StringField('Введите номер телефона', validators=[DataRequired()])
    personal_account = StringField('Введите номер лицевого счёта', validators=[DataRequired()])

    kitchen_hot_serial = StringField('Введите серийный номер счётчика горячей воды кухни',
                                      validators=[DataRequired()])
    kitchen_cold_serial = StringField('Введите серийный номер счётчика холодной воды кухни',
                                       validators=[DataRequired()])
    bathroom_hot_serial = StringField('Введите серийный номер счётчика горячей воды с/у',
                                       validators=[DataRequired()])
    bathroom_cold_serial = StringField('Введите серийный номер счётчика холодной воды с/у',
                                        validators=[DataRequired()])
    electricity_serial = StringField('Введите серийный номер счётчика электроэнергии',
                                      validators=[DataRequired()])

    kitchen_hot_last = StringField('Введите текущее показание счётчика горячей воды кухни',
                                      validators=[DataRequired()])
    kitchen_cold_last = StringField('Введите текущее показание счётчика холодной воды кухни',
                                       validators=[DataRequired()])
    bathroom_hot_last = StringField('Введите текущее показание счётчика горячей воды с/у',
                                       validators=[DataRequired()])
    bathroom_cold_last = StringField('Введите текущее показание счётчика холодной воды с/у',
                                        validators=[DataRequired()])
    electricity_last = StringField('Введите текущее показание счётчика электроэнергии',
                                      validators=[DataRequired()])

    submit = SubmitField('Сохранить')
