from datetime import date
from sqlalchemy.orm import Session
from app.models.user import RateLimit

DAILY_LIMIT = 20


def check_and_increment(neon_user_id: str, db: Session) -> bool:
    """Returns True if request is allowed, False if rate limited."""
    today = date.today()
    record = db.query(RateLimit).filter(
        RateLimit.neon_user_id == neon_user_id,
        RateLimit.request_date == today,
    ).first()

    if not record:
        record = RateLimit(neon_user_id=neon_user_id, request_date=today, request_count=1)
        db.add(record)
        db.commit()
        return True

    if record.request_count >= DAILY_LIMIT:
        return False

    record.request_count += 1
    db.commit()
    return True
