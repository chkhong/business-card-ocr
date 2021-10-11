import re
from loguru import logger
from typing import Tuple
import traceback

class EmailRecognition:
  def __init__(self):
    logger.debug(f'Initializing EmailRecognition...')

  def is_email(self, token:str) -> Tuple[bool, str]:
    success = False
    email = ''
    try:
      tok = token.lower()
      if (len(tok) >= 5 and tok.find("@") >= 0) or (tok.find("mail") >= 0 and len(tok) >= 11):
        success = True
        reg = re.compile(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')
        email = reg.search(token)[0]
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      if success:
        logger.info(f'''Found email: {email}, token: "{token}"''')
      return success, email


if __name__ == '__main__':
  test = EmailRecognition()
  string = 'E：sda  as kevin.ko@hkstp.org sdsss'
  logger.info(test.is_email(string))