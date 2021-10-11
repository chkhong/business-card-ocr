import re
from loguru import logger
from typing import Tuple
import traceback

class PhoneRecognition:
  def __init__(self):
    logger.debug(f'Initializing PhoneRecognition...')

  def is_phone(self, token:str) -> Tuple[bool, str]:
    success = False
    phone = ''
    try:
      m = re.findall(r'\d', token)
      if len(m) >= 8:
        success = True
        cond = [
          ['（', '('],
          ['）', ')'],
          [' ', ''],
        ]
        for c in cond:
          token = token.replace(c[0],c[1])
        reg = re.compile(r'\+?[0-9\(\)]{8,}')
        phone = reg.search(token)[0]
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      if success:
        logger.info(f'''Found phone_no: {phone}, token: "{token}"''')
      return success, phone

if __name__ == '__main__':
  test = PhoneRecognition()
  string = ''
  logger.info(test.is_phone(string))