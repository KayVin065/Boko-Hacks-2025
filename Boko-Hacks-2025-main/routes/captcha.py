from flask import Blueprint, send_file, session
from io import BytesIO
import random
import string
from utils.captcha import generate_captcha

captcha_bp = Blueprint("captcha", __name__)

@captcha_bp.route("/captcha/generate", methods=["GET"])
def get_captcha():
    """Generate a new CAPTCHA image - intentionally simplified"""
    # make arr of 8
    captchaArr = []
    result = ""
	
    # loops through and populates randomly as a number or a letter
    for i in range(8):
        if random.choice([True, False]):
            captchaArr.append(str(random.randint(0,9)))
        else:
            captchaArr.append(random.choice(string.ascii_letters))
        result += str(captchaArr[i])

    # captcha_text = "12345"
    captcha_text = result
    
    session["captcha_text"] = captcha_text
    
    image = generate_captcha(captcha_text)
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')