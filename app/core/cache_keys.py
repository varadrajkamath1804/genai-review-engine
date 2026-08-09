import hashlib


def review_sentiment_key(review: str) -> str:
    normalized_review = review.strip().lower()

    review_hash = hashlib.sha256(normalized_review.encode("utf-8")).hexdigest()

    return f"review:sentiment:{review_hash}"
