from flask import Blueprint

chat_v1 = Blueprint('chat_v1',
                    __name__,
                    template_folder='../../../templates',
                    static_folder='../../../static')

from app.api.v1.views import views  # noqa
