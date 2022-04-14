import os
from loguru import logger
import traceback
from typing import Tuple
from string_tools import StringTools


class AddressRecognition:

  def __init__(self):
    logger.debug(f'Initializing AddressRecognition...')
    self.common_address_token = []
    self.path = os.path.dirname(os.path.abspath(__file__))
    self.string_tools = StringTools()
    with open(self.path + '/../data/address_token', encoding='utf-8') as add_tokens:
      for token in add_tokens:
        normalize = token.strip().lower()
        if len(normalize) > 0:
          self.common_address_token.append(normalize)

  def is_address(self, line:str) -> Tuple[bool, str]:
    keyword_count = 1 # if keyword_count of tokens are address token, it is an address (consider the fact that some chinese name may include keywords in address token)
    success = False
    address = ''
    try:
      token = None
      if self.string_tools.isContainChinese(line):
        token = list(line)
        # logger.debug(f'address_token: {token}')
        keyword_count = 2
      else:
        token = line.split()
        # logger.debug(f'address_token: {token}')
      # if len(token) > 5:
      lower_line = line.lower()
      for add_token in self.common_address_token:
        if add_token in lower_line:
          keyword_count -= 1
          if keyword_count == 0:
            success = True
            address = line
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      if success:
        logger.info(f'''Found address: {address}, token: "{line}"''')
      return success, address


if __name__ == "__main__":
  test = AddressRecognition()
  logger.info(test.is_address('Unit 201, 16W, HKSTP, Shatin, Hong Kong'))
