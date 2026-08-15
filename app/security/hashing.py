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
        Verify a plain-text password against a stored bcrypt hash.

        bcrypt.checkpw() extracts the salt and cost factor from the stored
        hash, hashes the provided password using the same salt and settings,
        and compares the result with the stored hash.

        Returns:
            True  -> password matches
            False -> password does not match
        """

        return bcrypt.checkpw(
            plain_password.encode("utf-8"),  # User-entered password as bytes
            hashed_password.encode(
                "utf-8"
            ),  # Stored hash; gets the salt and checks with above password
        )
