from __future__ import annotations
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Jelszó", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Belépés")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Jelszó", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Regisztráció")

class SettingsForm(FlaskForm):
    default_list_id = IntegerField("Alap lista ID", validators=[Optional()])
    default_priority = SelectField("Alap prioritás", choices=[("1","1"),("2","2"),("3","3")], default="2")
    default_status = SelectField("Alap státusz", choices=[("TODO","TODO"),("DOING","DOING"),("DONE","DONE")], default="TODO")
    default_due_days = IntegerField("Alap határidő (nap)", validators=[NumberRange(min=0)], default=0)
    quick_add_fields = TextAreaField("Gyors rögzítés mezők (JSON lista)", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Mentés")
