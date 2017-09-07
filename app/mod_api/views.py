from flask import (
    Blueprint
)
from .models import *

mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.route('/', methods=['GET'])
def index():
    return 'its ok'