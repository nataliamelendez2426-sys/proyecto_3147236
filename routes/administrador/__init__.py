from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='admin')


from . import routes
