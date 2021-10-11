from loguru import logger
import traceback
from difflib import SequenceMatcher

class StringTools:
  def __init__(self):
    logger.debug(f'Initialising StringTools...')

  def isContainChinese(self, s:str) -> bool: #check if string contains chinese character
    try:
      for c in s:
        if ('\u4e00' <= c <= '\u9fa5'):
          return True
      return False
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())

  def similar(self, a:str, b:str) -> int:
    return SequenceMatcher(None, a, b).ratio()

if __name__ == '__main__':
  test = StringTools()
  logger.info(test.similar('高建荣','高建榮'))