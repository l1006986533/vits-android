""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from pypinyin import Style, pinyin
from pypinyin.style._utils import get_finals, get_initials
# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text

def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text

def chinese_cleaners1(text):
    from pypinyin import Style, pinyin

    phones = [phone[0] for phone in pinyin(text, style=Style.TONE3)]
    return ' '.join(phones)
  
  
def chinese_cleaners2(text):
  phones = [
      p
      for phone in pinyin(text, style=Style.TONE3)
      for p in [
          get_initials(phone[0], strict=True),
          get_finals(phone[0][:-1], strict=True) + phone[0][-1]
          if phone[0][-1].isdigit()
          else get_finals(phone[0], strict=True)
          if phone[0][-1].isalnum()
          else phone[0],
      ]
      # Remove the case of individual tones as a phoneme
      if len(p) != 0 and not p.isdigit()
  ]
  return phones
  # return phonemes
  
if __name__ == '__main__':
  res = chinese_cleaners2('这是语音测试！')
  print(res)
  res = chinese_cleaners1('"第一，南京不是发展的不行，是大家对他期望很高，')
  print(res)
  
  # english_cleaners2 deleted
  # res = english_cleaners2('this is a club test for one train.GDP')
  # print(res)