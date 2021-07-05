


# methods
def translate_list_hg19_to_hg38(region_list, debug=False):
    ''' method to translate from hg19 to hg38 genome reference '''
    # initialize
    result = []
    debug = []

    # translate
    for item in region_list:
        chrom = item['chrom']
        start = item['start']
        end = item['end']

        # get the result for the item
        translated = translate_region_hg19_to_hg38(chrom, start, end, debug)

        # append the result
        result += translated
        debug += {"input": item, "output": translated}
            
    # return
    return result, debug


def translate_region_hg19_to_hg38(chrom, start, end, debug=False):
    ''' method to translate from hg19 to hg38 genome reference '''
    # initialize
    result = []

    # translate

    # return
    return result


