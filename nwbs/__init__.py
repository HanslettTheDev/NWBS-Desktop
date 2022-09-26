from datetime import datetime

def logCode() -> tuple[str, str]:
    t = datetime.now().strftime("%Y-%m-%d")
    cctime = datetime.now().strftime("%H-%M-%S")
    return t, str(cctime)