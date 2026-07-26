import bcrypt


class PasswordHasher:
    """
    Handles password hashing and verification.
    """

    @staticmethod
    def hash_password(
        password: str,
    ) -> str:
        """
        Convert a plain password into a secure bcrypt hash.
        """

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        )

        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain password against a stored bcrypt hash.
        """

        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
