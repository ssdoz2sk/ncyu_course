from itsdangerous import URLSafeTimedSerializer
import base64

class Token():
    def __init__(self, security_key, method):
        self.security_key = security_key
        self.method = method
        self.salt = security_key

    def generate_validate_token(self, username):
        serializer = URLSafeTimedSerializer(self.security_key)
        return serializer.dumps({'username': username, 'method': self.method }, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(self.security_key)
        data = serializer.loads(token,
                                salt=self.salt,
                                max_age=expiration)
        if data['method'] != self.method:
            raise TokenMethodError

        return data['username']


class TokenMethodError(Exception):
    pass

