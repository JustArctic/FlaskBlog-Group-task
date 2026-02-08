from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    tags = HiddenField('Tags')
    submit = SubmitField('Post')


class CommentForm(FlaskForm): 
    content = TextAreaField('Share your thoughts...', validators=[DataRequired()])
    submit = SubmitField('Post Comment')