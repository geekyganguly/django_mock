import secrets
import string

class Generator:
    """
    Helper class for Generator utilities.
    """
    @staticmethod
    def generate_string(size=6, chars=string.ascii_letters):
        return ''.join(secrets.choice(chars) for _ in range(size))

    @staticmethod
    def generate_username(size=8):
        return Generator.generate_string(size=size, chars=string.ascii_uppercase + string.digits)
