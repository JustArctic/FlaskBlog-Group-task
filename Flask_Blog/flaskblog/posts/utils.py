import os
import secrets
from PIL import Image
from flask import current_app

def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

TAG_LABELS = {
    'beef': 'Beef',
    'chicken': 'Chicken',
    'fish': 'Fish',
    'veggie': 'Veggie',
    'easy': 'Amateur',
    'medium': 'Proficient',
    'hard': 'Expert',
    'quick': 'Quick',
    'moderate': 'Moderate',
    'slow': 'Slow'
}
