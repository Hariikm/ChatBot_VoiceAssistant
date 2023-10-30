from Thrisha_Assistant import logger
from Thrisha_Assistant.components import AllCode

assistant= AllCode

try:
    assistant.run_code()


except Exception as e:
    logger.exception(e)
    raise e