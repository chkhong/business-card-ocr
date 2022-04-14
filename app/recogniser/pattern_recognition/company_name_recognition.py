import os

class CompanyNameRecognition:
  def __init__(self):
    self.path = os.path.dirname(os.path.abspath(__file__))
    self.common_company_tokens = []
    with open(self.path + '/../data/common_prefix_suffix_company') as company_tokens:
      for token in company_tokens:
        comp_token = token.strip().lower()
        if len(comp_token) > 0:
          self.common_company_tokens.append(comp_token)


  def is_company_name(self, line):
    line = line.lower().split(' ')
    for token in self.common_company_tokens:
      if line.__contains__(token):
        return True
    return False