from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, TextAreaField, FileField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional
from app.models.user import User
from app.models.prompt import Prompt
from app.models.model import Model
from wtforms.widgets import ListWidget, CheckboxInput, NumberInput

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField('Repita a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um nome de usuário diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um email diferente.')

class PromptForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    text = TextAreaField('Texto', validators=[DataRequired()])
    role = SelectField('Role', choices=[('', ''), ('SYSTEM', 'SYSTEM'), ('USER', 'USER'), ('ASSISTANT', 'ASSISTANT')], validators=[Optional()])
    temperature = FloatField('Temperatura', validators=[Optional()], widget=NumberInput(min=0, max=1, step=0.01))
    categories = SelectMultipleField('Categorias', coerce=int)
    model = SelectField('Modelo', coerce=int)
    json_file = FileField('JSON', validators=[Optional()])
    submit = SubmitField('Salvar')

class CategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Adicionar')

class ModelForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Adicionar')
