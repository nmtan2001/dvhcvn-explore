import pytest
from main import data_explore, total, remove_diacritics, get_country

country = get_country()

def test_get_country():
    assert type(country) == dict
    
def test_total():
    assert total(country) == (63, 705, 10598)

def test_remove():
    assert remove_diacritics('Thành phố Cần Thơ') == 'Thanh pho Can Tho'

def test_data_explore():
    assert data_explore(country,'Thành phố Hà Nội') == 'Number of districts and communes for Thành phố Hà Nội: 30 districts, 579 communes'
    assert data_explore(country, 'Thành phố Hà Nội', 'Quận Ba Đình') == 'Number of communes for Quận Ba Đình of Thành phố Hà Nội : 14 communes'


