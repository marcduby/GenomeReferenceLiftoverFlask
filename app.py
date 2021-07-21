
from flask import Flask, request, jsonify
from utils import translate_list_hg19_to_hg38, translate_ld_server_input_hg19_to_hg38

app=Flask(__name__)

@app.route('/')
def test():
    return "This is a Genome Liftover REST service"


@app.route('/liftover', methods=['POST'])
def liftover():
    ''' method accepts list of region chr/start/end tuples to convert from hg19 to hg38; will return list of converted region positions '''
    # initialize
    result = []

    # get the payload
    input = request.json
    regions_input = input.get('regions')

    # log
    print("got input: {}".format(regions_input))

    # get the translation
    result, debug = translate_list_hg19_to_hg38(region_list=regions_input, debug=True)
    print("app DEBUG: {}".format(debug))

    # log
    print("got payload: \n{}".format(input))

    # return
    return jsonify({"regions": result, "debug": debug})

@app.route('/ld_server_liftover', methods=['POST'])
def ld_server_liftover():
    ''' method accepts ld server format input, translates the regions in it, and returns the result in ld server format '''
    # initialize
    result = []

    # get the payload
    input = request.json

    # log
    print("got input: {}".format(input))

    # get the translation
    result = translate_ld_server_input_hg19_to_hg38(input_ld_server_map=input, debug=True)

    # log
    print("got result: \n{}".format(result))

    # return
    return jsonify(result)


if __name__ == "__main__":
    # start the application
    app.run(port=7070)

