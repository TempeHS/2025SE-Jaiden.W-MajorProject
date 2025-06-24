from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, DateTimeField, SelectField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

def has_uppercase(_form, field):
    if not any(char.isupper() for char in field.data):
        raise ValidationError('Password must contain at least one uppercase letter.')

def has_lowercase(_form, field):
    if not any(char.islower() for char in field.data):
        raise ValidationError('Password must contain at least one lowercase letter.')

def has_digit(_form, field):
    if not any(char.isdigit() for char in field.data):
        raise ValidationError('Password must contain at least one digit.')

def has_special_char(_form, field):
    if not any(char in '@$!%*?&#' for char in field.data):
        raise ValidationError('Password must contain at least one special character (@$!%*?&).')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25), 
        Regexp(r'^[\w.@+-]+$', message="Username must contain only letters, numbers, and @/./+/-/_ characters.")
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField('Log In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25), 
        Regexp(r'^[\w.@+-]+$', message="Username must contain only letters, numbers, and @/./+/-/_ characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=120),
        Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$', message="Enter a valid email address.")
    ])
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=128),
        has_uppercase,
        has_lowercase,
        has_digit,
        has_special_char
    ])
    role = RadioField('Role', choices=[('Player', 'Player'), ('Coach', 'Coach')], default='Player', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class TwoFactorForm(FlaskForm):
    token = StringField('2FA Token', validators=[DataRequired()])
    submit = SubmitField('Verify')

class JoinTeamForm(FlaskForm):
    submit = SubmitField('Join Team')

class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[
        DataRequired(), 
        Length(min=2, max=50), 
        Regexp(r'^[\w\s]+$', message="Team name must contain only letters, numbers, and spaces.")
    ])
    team_description = StringField('Team Description', validators=[
        DataRequired(), 
        Length(max=200)
    ])
    submit = SubmitField('Create Team')

class TeamEventForm(FlaskForm):
    title = StringField('Event Title', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500)
    ])
    event_date = DateTimeField('Event Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()], render_kw={"type": "datetime-local"})
    location = StringField('Location', validators=[
        DataRequired(),
        Length(max=100)
    ])
    recurrence = SelectField('Repeat', choices = [
        ('none', 'No Repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ], default='none')
    recurrence_end = DateField('Repeat Until', format='%Y-%m-%d', render_kw={"type": "date"})
    submit = SubmitField('Create Event')

class DeleteEventForm(FlaskForm):
    submit = SubmitField('Delete')

class AttendanceForm(FlaskForm):
    status = SelectField('Attendance', choices=[('attending', 'Yes, I will attend'), ('not_attending', 'No, I cannot attend')])
    submit = SubmitField('Submit')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete my Data')

class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=120),
        Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$', message="Enter a valid email address.")
    ])
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    role = RadioField('Role', choices=[('Player', 'Player'), ('Coach', 'Coach')], validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, max=128),
        has_uppercase,
        has_lowercase,
        has_digit,
        has_special_char
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.new_password.data != self.confirm_password.data:
            self.confirm_password.errors.append('New passwords must match.')
            return False
        return True
