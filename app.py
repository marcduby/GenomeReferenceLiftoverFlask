
from flask import Flask, request, jsonify


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

    # log
    print("got payload: \n{}".format(input))

    # return
    return jsonify({"regions": result})


if __name__ == "__main__":
    # start the application
    app.run(port=7070)

