

# constants
CHROM = 'chrom'
START = 'start'
END = 'end'


# methods
def translate_list_hg19_to_hg38(region_list, debug=False):
    ''' method to translate from hg19 to hg38 genome reference '''
    # initialize
    result = []
    debug = []

    # translate
    for item in region_list:
        chrom = item[CHROM]
        start = item[START]
        end = item[END]

        # get the result for the item
        translated = translate_region_hg19_to_hg38(chrom, start, end, debug)

        # append the result
        result += translated
        temp_dict = {"input": item, "output": translated}
        debug.append(temp_dict)
        print("DEBUG dict: {}".format(temp_dict))
        print("DEBUG: {}".format(debug))
            
    # return
    return result, debug


def translate_region_hg19_to_hg38(chrom, start, end, debug=False):
    ''' method to translate from hg19 to hg38 genome reference '''
    # initialize
    result = []

    # translate
    # TODO - use crossmap
    item = {}
    item[CHROM] = chrom
    item[START] = end
    item[END] = start
    result.append(item)
    
    # return
    return result


