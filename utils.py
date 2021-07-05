
# imports
from cmmodule.utils     import read_chain_file
from cmmodule.utils import map_coordinates

# constants
CHROM = 'chrom'
START = 'start'
END = 'end'
FILE_MAPPING = "Data/hg19ToHg38.over.chain.gz"

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
    result = liftover_locus(chrom, start, end)
    # item = {}
    # item[CHROM] = chrom
    # item[START] = end
    # item[END] = start
    # result.append(item)
    
    # return
    return result


def liftover_locus(chrom, start, end, debug=False):
    ''' method copied from the bed file translation from the CrossMap library '''
    strand = '+'
    fields = [chrom, start, end]
    result = []

    # get the mapping 
    mapping = get_chain_map(FILE_MAPPING)

    # get the mapped coorfdinates
    a = map_coordinates(mapping, chrom, start, end, strand)

    try:
        if (a is None) or (len(a) % 2 != 0):
            result = None
            
        # copied from crossmap code; unclear why two statements
        # TODO - try replacing with len(a) >= 2
        if len(a) == 2:
            if debug:
                print("for {}/{}/{} got : {}".format(chrom, start, end, a))
            mapped_region = get_mapped_fields(a[1])
            result.append(mapped_region)            

        if len(a) >2 :
            # count=0
            for j in range(1,len(a),2):
                if debug:
                    print("for {}/{}/{} got : {}".format(chrom, start, end, a))
                mapped_region = get_mapped_fields(a[j])
                result.append(mapped_region)            

                # if outfile is None:
                #     print(line + '\t'+ '(split.' + str(count) + ':' + ':'.join([str(i) for i in a[j-1]]) + ')\t' + '\t'.join([str(i) for i in fields]))
                # else:
                #     print('\t'.join([str(i) for i in fields]), file=FILE_OUT)

    except:
        print("got mapping error for chrom: {}, start: {}, end: {}".format(chrom, start, end))

    # return
    return result

def get_mapped_fields(mapped, debug=False):
    ''' method to take a mapped result and translate into our format '''
    chrom = mapped[0]
    start = mapped[1]
    end = mapped[2]

    # format
    result = {CHROM: chrom, START: start, END: end}

    # return
    return result


def get_chain_map(file_location, debug=False):
    ''' method to get the chanin map from the chain file '''
    map_chain = None

    # get the chain map
    (map_chain, targetChromSizes, sourceChromSizes) = read_chain_file(file_location)

    # return 
    return map_chain
