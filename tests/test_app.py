from nose.tools import *

from ..app import address_parts

@raises(TypeError)
def test_address_parts_no_address():
  expected = []
  actual = address_parts()

def test_address_parts_with_address():
  expected = ['AddressNumber', 'StreetName']
  actual = address_parts('123 main')
  assert actual == expected
