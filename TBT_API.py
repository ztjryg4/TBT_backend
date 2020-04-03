from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS

import json

import TBT_func

app = Flask(__name__)

CORS(app, supports_credentials=True)

@app.route('/routest', methods=['post','get'])
def routetResponse():
    dep_starts = request.get_json()
    print(dep_starts["dep_starts"])
    return dep_starts

@app.route('/routes', methods=['post','get'])
def routeResponse():
    data = request.get_json()
    mode = data['mode']
    if mode == "both":
        dep_starts = data['dep_starts']
        dep_ends = data['dep_ends']
        vehicle_capacities = data['vehicle_capacities']
        if not all([dep_starts, dep_ends, vehicle_capacities]):
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            # js = TBT_func.case1(dep_starts, dep_ends, vehicle_capacities)
            # res = Response(js, status=200, mimetype='application/json')
            # return res
            try:
                js = TBT_func.case1(dep_starts, dep_ends, vehicle_capacities)
            except:
                js = TBT_func.ErrorGen("TBT Unknow Error.")
                res = Response(js, status=200, mimetype='application/json')
                return res
            else:
                res = Response(js, status=200, mimetype='application/json')
                return res
    elif mode == "num":
        dep_starts = data['dep_starts']
        dep_ends = data['dep_ends']
        num_vehicles = data['num_vehicles']
        if not all([dep_starts, dep_ends, num_vehicles]):
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            # js = TBT_func.case2(dep_starts, dep_ends, num_vehicles)
            # res = Response(js, status=200, mimetype='application/json')
            # return res
            try:
                js = TBT_func.case2(dep_starts, dep_ends, num_vehicles)
            except:
                js = TBT_func.ErrorGen("TBT Unknow Error.")
                res = Response(js, status=200, mimetype='application/json')
                return res
            else:
                res = Response(js, status=200, mimetype='application/json')
                return res
    elif mode == "cap":
        depot = data['depot']
        vehicle_capacities = data['vehicle_capacities']
        if (not all([depot, vehicle_capacities])) and depot != 0:
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            try:
                js = TBT_func.case3(depot, vehicle_capacities)
            except:
                js = TBT_func.ErrorGen("TBT Unknow Error.")
                res = Response(js, status=200, mimetype='application/json')
                return res
            else:
                res = Response(js, status=200, mimetype='application/json')
                return res
    else:
        js = TBT_func.ErrorGen("TBT Mode Error.")
        res = Response(js, status=200, mimetype='application/json')
        return res

@app.route('/preset/', methods=['get'])
def presetResponse():
    param = request.args.get('id')
    res = param
    return res

if __name__ == "__main__":
    # app.run(host="0.0.0.0",debug=True,port=2019)
    app.run(debug=True, port=2019)