import traceback
from loguru import logger

from recogniser.pattern_recognition.address_recognition import AddressRecognition
from recogniser.pattern_recognition.email_recognition import EmailRecognition
from recogniser.pattern_recognition.phone_recognition import PhoneRecognition
from recogniser.pattern_recognition.name_recognition import NameRecognition


class BusinessCardClassifier:
  def __init__(self):
    self.address_rec = AddressRecognition()
    self.email_rec = EmailRecognition()
    self.phone_rec = PhoneRecognition()
    self.name_rec = NameRecognition()

  def classify(self, tokens:list) -> dict:
    result = {'name':'', 'last_name': '', 'first_name':'', 'contact_number':[],'address':[], 'email':[]}
    try:
      for token in tokens:
        is_address, address = self.address_rec.is_address(token)
        if is_address:
          result['address'].append(address)
          continue
        is_email, email = self.email_rec.is_email(token)
        if is_email:
          result['email'].append(email)
          continue
        is_phone, phone = self.phone_rec.is_phone(token)
        if is_phone:
          result['contact_number'].append(phone)
          continue
        is_name, name, lastname, firstname = self.name_rec.is_name(token)
        if is_name:
          result['name'] = name
          result['last_name'] = lastname
          result['first_name'] = firstname
          continue
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
    finally:
      return result


if __name__ == "__main__":
  test = BusinessCardClassifier()
  list = ['AStraZeneca', 'caringcompan', 'www.astrazeneca.com.hk', 'hugo.tan@astrazeneca.com', '阿斯利康', '陳德威', '商界展關懷', '阿斯利康香港有限公司', '香港北角京華道18號11樓1-3室', '電話：+85224207388', '直視：+85229415206', '傳真：+852301019783', '手標：+85256828878']
  result = test.classify(list)
  logger.info(result)