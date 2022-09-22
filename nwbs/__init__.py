from datetime import datetime
import random

def logCode() -> tuple[str, str]:
    t = datetime.now().strftime("%Y-%m-%d")
    log_code = random.randint(10000, 99999)
    return t, str(log_code)