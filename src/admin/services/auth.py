from flask_basicauth import BasicAuth
from werkzeug import Response
from werkzeug.exceptions import HTTPException

from admin.app import app


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                "You could not be authenticated. Please refresh the page.",
                status=401,
                headers={'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        )


basic_auth = BasicAuth(app)
