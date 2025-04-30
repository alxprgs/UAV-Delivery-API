from datetime import datetime, timedelta, timezone
import time

def get_unix_timestamp() -> int:
    return round(time.time())

def get_formatted_timestamp() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime('%H:%M:%S %d.%m.%Y')

def token_expiration_time(days: int = 3) -> int:
    expiration_time = datetime.now(timezone.utc) + timedelta(days=days)
    return int(expiration_time.timestamp())