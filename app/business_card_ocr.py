from loguru import logger
import traceback
from paddleocr import PaddleOCR
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
from recogniser.business_card_classifier import BusinessCardClassifier
from string_tools import StringTools
import os
from typing import Tuple

SIMILAR_THRESHOLD = 0.5

class BusinessCardOCR:
  def __init__(self):
    logger.debug('-'*100)
    logger.debug(f'Initializing BusinessCardOCR Class')
    self.path = os.path.dirname(os.path.abspath(__file__))
    self.ocr_chs = PaddleOCR(use_angle_cls=True, lang='ch') # need to run only once to download and load model into memory
    self.ocr_cht = PaddleOCR(use_angle_cls=True, lang='chinese_cht') # need to run only once to download and load model into memory
    self.bc_classify = BusinessCardClassifier()
    self.string_tools = StringTools()


  def detect_recognise_text(self, filepath:str=''):
    '''
    @param filepath: path of file that is needed for text detection and recognition
    '''
    result = []
    result_chs:list = []
    result_cht:list = []
    try:
      logger.debug(f'Running detect_recognise_text() ...')
      result_chs = self.ocr_chs.ocr(filepath, cls=False)
      result_cht = self.ocr_cht.ocr(filepath, cls=False)
      # result_chs yield better english and simplified chinese result
      # result_cht yield better trasitional chinese result

      logger.debug('-'*100)
      logger.info(f'Identifying more accurate term...')
      for r_chs in result_chs:
        for r_cht in result_cht:
          # logger.debug(r_chs)
          # logger.debug(r_cht)
          chs = r_chs[1][0]
          cht = r_cht[1][0]
          logger.debug(f'chs: {chs}, cht: {cht}')
          if self.string_tools.similar(chs, cht) >= SIMILAR_THRESHOLD:
            if not self.string_tools.isContainChinese(chs):
              result.append(chs)
              logger.debug(f'chose chs: {chs}')
              result_cht.remove(r_cht)
              break
            elif self.string_tools.isContainChinese(cht):
              result.append(cht)
              logger.debug(f'chose cht: {cht}')
              result_cht.remove(r_cht)
              break
      logger.info(f'Extracted info: {result}')
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      return result
      
  def classify(self, list:list) -> dict:
    return self.bc_classify.classify(list)

  def analyse(self, filepath:str='') -> dict:
    result = {}
    try:
      text = self.detect_recognise_text(filepath)
      result = self.bc_classify.classify(text)
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      return result

  def analyse_file(self, file_object:object) -> Tuple[bool, str, dict]:
    accepted_extension = ['.jpeg', '.jpg', '.png']
    success = False
    message = ''
    result = {}
    try:
      for acc_ext in accepted_extension:
        if acc_ext in file_object.filename:
          new_file_location = f'{file_object.filename}'
          logger.warning(new_file_location)
          with open(new_file_location, "wb+") as f:
            f.write(file_object.file.read())
          result = self.analyse(new_file_location)
          os.remove(new_file_location)
          break
      else:
        message = f'''File extension is not supported! Supported file extension: {accepted_extension}'''
      if result:
        success = True
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      return success, message, result

if __name__ == '__main__':
    filepath = '../test/cn2.jpeg'
    ocr = BusinessCardOCR()
    logger.info(ocr.analyse(filepath))
    logger.info(f'End of main()...')
  
