from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


class Hash:
    @staticmethod
    def bcrypt(password: str):
        """Get hash from password"""
        return password_context.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        """Verify hash with password"""
        return password_context.verify(plain_password, hashed_password)
