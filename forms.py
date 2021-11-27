from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError,Regexp
from models.models import *

class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(message="이메일 형식이 아닙니다.")])
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20, message="비밀번호는 8자리 이상이어야 합니다.")])
    password_check = PasswordField('password_check', validators=[DataRequired(), EqualTo('password', message="비밀번호 확인이 다릅니다.")])
    submit = SubmitField('회원가입')
    
    def validate_name(self, name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in name.data:
            if char in excluded_chars:
                raise ValidationError(f"이름은 한글/영어로만 이루어져야 합니다. (특수기호 X)")
    
    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError("이미 존재하는 이메일입니다.")
    
        
class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(message="이메일 형식이 아닙니다.")])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("로그인")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("없는 이메일입니다.")
        
class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('current_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired(), Length(min=8, max=20, message="비밀번호는 8자리 이상이어야 합니다.")])
    password_check = PasswordField('password_check', validators=[DataRequired(), EqualTo('new_password', message="비밀번호 확인이 다릅니다.")])
    submit = SubmitField("비밀번호 변경하기")