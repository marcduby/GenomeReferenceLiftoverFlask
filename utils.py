
# imports
from cmmodule.utils     import read_chain_file
from cmmodule.utils import map_coordinates
import copy

# constants
CHROM = 'chrom'
START = 'start'
END = 'stop'
MASK_DEFINITIONS = 'maskDefinitions'
GROUPS = 'groups'
FILE_MAPPING_HG19_HG38 = "Data/hg19ToHg38.over.chain.gz"

# data
# get the hg19/hg38 chain map
(map_chain_hg19_hg38, targetChromSizes, sourceChromSizes) = read_chain_file(FILE_MAPPING_HG19_HG38)

# methods
def translate_ld_server_input_hg19_to_hg38(input_ld_server_map, debug=False):
    ''' will take ld server input format, ligtover regions, return in ld server format '''
    # initialize
    result_ld_server = copy.deepcopy(input_ld_server_map)
    chrom = None
    masks = None
    groups = None 
    new_groups = {}

    # build a list of the regions
    chrom = input_ld_server_map.get(CHROM)
    masks = input_ld_server_map.get(MASK_DEFINITIONS)
    if chrom and masks:
        for (mask_index, mask_item) in enumerate(masks):
            groups = masks[mask_index].get(GROUPS)
            if groups:
                # all in order, translate top level region first, then groups
                start = input_ld_server_map.get(START)
                stop = input_ld_server_map.get(END)
                if start and stop:
                    translated = translate_region_hg19_to_hg38(chrom, start, start)
                    if translated and len(translated) > 0:
                        result_ld_server[START] = translated[0][START]
                    translated = translate_region_hg19_to_hg38(chrom, stop, stop)
                    if translated and len(translated) > 0:
                        result_ld_server[END] = translated[0][END]

                # translate the regions
                new_groups = {}
                print(groups)
                for key, value in groups.items():
                    start = value.get(START)
                    stop = value.get(END)
                    translated = translate_region_hg19_to_hg38(chrom, start, stop)

                    for (group_index, group_item) in enumerate(translated):
                        new_groups[key + str(group_index)] = {START: group_item.get(START), END: group_item.get(END)}

                # replace the translated regions on the results
                result_ld_server[MASK_DEFINITIONS][mask_index][GROUPS] = new_groups

    # return
    return result_ld_server

def translate_list_hg19_to_hg38(region_list, debug=False):
    ''' 
    method to translate list of regions from hg19 to hg38 genome reference 
    input - list of {chrom: <value>, start: <value>, stop: <value>}
    output - list of {chrom: <value>, start: <value>, stop: <value>}
    '''
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
        print("DEBUG temp dict: {}".format(temp_dict))
        print("DEBUG: {}".format(debug))
            
    # return
    print("DEBUG: return {}".format(debug))
    return result, debug


def translate_region_hg19_to_hg38(chrom, start, end, debug=False):
    ''' 
    method to translate a region from hg19 to hg38 genome reference 
    input - {chrom: <value>, start: <value>, stop: <value>}
    output - list of {chrom: <value>, start: <value>, stop: <value>}
    '''
    # initialize
    result = []

    # translate
    # TODO - use crossmap
    if chrom and start and end:
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
    # mapping = get_chain_map(FILE_MAPPING)
    mapping = map_chain_hg19_hg38

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
    ''' method to get the chain map from the chain file '''
    map_chain = None

    # get the chain map
    (map_chain, targetChromSizes, sourceChromSizes) = read_chain_file(file_location)

    # return 
    return map_chain
