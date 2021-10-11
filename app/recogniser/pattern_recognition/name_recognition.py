import os
from difflib import SequenceMatcher
from loguru import logger
import traceback
import re
from hanziconv import HanziConv
from typing import Tuple, Dict
from string_tools import StringTools

MIN_LENGTH = 5

class NameRecognition:


  def __init__(self):
    logger.debug(f'Initializing NameRecognition...')
    self.path = os.path.dirname(os.path.abspath(__file__))
    self.string_tools = StringTools()
    self.common_name_en = []
    self.lastname_double_ch = []
    self.lastname_ch = []
    # Load data
    with open(self.path + '/../data/lastname_hk_en', 'r') as lastname_hk_en:
      for line in lastname_hk_en:
        name = line.strip()
        self.common_name_en.append(name)
    with open(self.path + '/../data/common_name_en', 'r') as en_name:
      for line in en_name:
        name = line.strip()
        if len(name) >= MIN_LENGTH:
          self.common_name_en.append(name)
    with open(self.path + '/../data/lastname_double_hk_ch', 'r', encoding='utf8') as lastname_double_hk_ch:
      for line in lastname_double_hk_ch:
        name = line.strip()
        self.lastname_double_ch.append(name)
    with open(self.path + '/../data/lastname_hk_ch', 'r', encoding='utf8') as lastname_hk_ch:
      for line in lastname_hk_ch:
        name = line.strip()
        self.lastname_ch.append(name)

  def find_lastname_en(self, token:str) -> str:
    tok = token.lower().split()
    for lastname in reversed(tok): # to search last token first, surname tend to be last in naming convention
      for list in self.common_name_en:
        if lastname == list:
          logger.debug(f'Found lastname: {lastname}')
          return lastname


  # Find highest probability of a token may be a name
  def find_best_guessed_name(self, tokens):
    pass

  def find_lastname_ch(self, token:str) -> str:
    try:
      tok = HanziConv.toSimplified(token)
      lastname = tok[0:2]
      if any(lastname in list for list in self.lastname_double_ch):
        return token[0:2]
      lastname = tok[0]
      if any(lastname in list for list in self.lastname_ch):
        return token[0]
      return ''
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())


  def is_ch_name(self, token:str) -> Tuple[bool, str, str]: # return bool, if name is chinese
    success = False
    lastname = ''
    firstname = ''
    try:
      if len(token) >= 2 and len(token) <= 4: # normal chinese name length between 2 - 4
        lastname = self.find_lastname_ch(token)
        if lastname:
          firstname = token[len(lastname):]
          success = True
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      return success, lastname, firstname


  def is_en_name(self, token:str) -> Tuple[bool, str, str]:
    success = False
    lastname = ''
    firstname = ''
    try:
      token = token.lower()
      if len(token.split()) > 5:
        logger.debug(f'Input is too long to be a name')
        return success, lastname, firstname
      lastname = self.find_lastname_en(token)
      if lastname:
        firstname = token.replace(lastname, '').replace('  ', ' ').strip()
        success = True
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      return success, lastname, firstname


  def is_name(self, token:str) -> Tuple[bool, str, str, str]:
    success = False
    name = ''
    firstname = ''
    lastname = ''
    try:
      reg = re.compile(r'[a-zA-Z\u4e00-\u9fa5 ]') 
      tok = list(token)
      for t in tok:
        if not reg.match(t): #return false if any char contains non Chinese or English char
          break
      else:
        if self.string_tools.isContainChinese(token):
          success, lastname, firstname = self.is_ch_name(token)
          if success:
            name = token
        else:
          success, lastname, firstname = self.is_en_name(token)
          if success:
            lastname = lastname.capitalize()
            firstname = firstname.capitalize()
            name = token
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      if success:
        logger.info(f'''Found name: {name}, lastname: {lastname}, firstname: {firstname}, token: "{token}"''')
      return success, name, lastname, firstname


if __name__ == '__main__':
  test = NameRecognition()
  string = '陳德威'
  logger.info(test.is_name(string))