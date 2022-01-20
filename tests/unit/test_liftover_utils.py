# imports
import pytest 
from utils import translate_list_hg19_to_hg38, translate_region_hg19_to_hg38

def test_translate_region_list():
    ''' 
    test the translation of list of regions
    '''
    # build the test data
    list_region = [{'chrom': '3', 'start': 12678867, 'stop': 12925855}, {'chrom': '3', 'start': 12278867, 'stop': 12525855}]
    assert len(list_region) == 2

    # test the translation function
    list_result, debug = translate_list_hg19_to_hg38(region_list=list_region, debug=False)
    assert len(list_result) == 3

def test_translate_region():
    ''' 
    test the translation of individual regions
    '''
    # build the test data
    region1 = {'chrom': '3', 'start': 12678867, 'stop': 12925855}
    region2 = {'chrom': '3', 'start': 12278867, 'stop': 12525855}

    # test the translation function on the first region
    list_result = translate_region_hg19_to_hg38(chrom=region1.get('chrom'), start=region1.get('start'), end=region1.get('stop'), debug=False)
    assert len(list_result) == 2

    # test the translation function on the second region
    list_result = translate_region_hg19_to_hg38(chrom=region2.get('chrom'), start=region2.get('start'), end=region2.get('stop'), debug=False)
    assert len(list_result) == 2
