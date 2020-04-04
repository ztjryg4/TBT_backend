from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS

import json

import TBT_func
import TBT_preset

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
        # case1: 
        # distance_matrix, demands, dep_starts, dep_ends, vehicle_capacities
        distance_matrix = data['distance_matrix']
        demands = data['demands']
        dep_starts = data['dep_starts']
        dep_ends = data['dep_ends']
        vehicle_capacities = data['vehicle_capacities']
        if not all([distance_matrix, demands, dep_starts, dep_ends, vehicle_capacities]):
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            # js = TBT_func.case1(distance_matrix, demands, dep_starts, dep_ends, vehicle_capacities)
            # res = Response(js, status=200, mimetype='application/json')
            # return res
            try:
                js = TBT_func.case1(distance_matrix, demands, dep_starts, dep_ends, vehicle_capacities)
            except:
                js = TBT_func.ErrorGen("TBT Unknow Error.")
                res = Response(js, status=200, mimetype='application/json')
                return res
            else:
                res = Response(js, status=200, mimetype='application/json')
                return res
    elif mode == "num":
        # distance_matrix, demands, dep_starts, dep_ends, num_vehicles
        distance_matrix = data['distance_matrix']
        demands = data['demands']
        dep_starts = data['dep_starts']
        dep_ends = data['dep_ends']
        num_vehicles = data['num_vehicles']
        if not all([distance_matrix, demands, dep_starts, dep_ends, num_vehicles]):
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            # js = TBT_func.case2(distance_matrix, demands, dep_starts, dep_ends, num_vehicles)
            # res = Response(js, status=200, mimetype='application/json')
            # return res
            try:
                js = TBT_func.case2(distance_matrix, demands, dep_starts, dep_ends, num_vehicles)
            except:
                js = TBT_func.ErrorGen("TBT Unknow Error.")
                res = Response(js, status=200, mimetype='application/json')
                return res
            else:
                res = Response(js, status=200, mimetype='application/json')
                return res
    elif mode == "cap":
        # distance_matrix, demands, depot, vehicle_capacities
        distance_matrix = data['distance_matrix']
        demands = data['demands']
        depot = data['dep_starts'][0]
        vehicle_capacities = data['vehicle_capacities']
        if (not all([distance_matrix, demands, depot, vehicle_capacities])) and depot != 0:
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            # js = TBT_func.case3(distance_matrix, demands, depot, vehicle_capacities)
            # res = Response(js, status=200, mimetype='application/json')
            # return res
            try:
                js = TBT_func.case3(distance_matrix, demands, depot, vehicle_capacities)
            except:
                js = TBT_func.ErrorGen("TBT Unknow Error.")
                res = Response(js, status=200, mimetype='application/json')
                return res
            else:
                res = Response(js, status=200, mimetype='application/json')
                return res
    elif mode == "takeaway":
        # distance_matrix, dep_starts, pickups_deliveries, pick_weights='', weight_limits=''
        # case4(distance_matrix, dep_starts, pickups_deliveries, pick_weights='', weight_limits='')
        distance_matrix = data['distance_matrix']
        dep_starts = data['dep_starts']
        pickups_deliveries = data['pickups_deliveries']
        pick_weights = data['pick_weights']
        weight_limits = data['weight_limits']

        print(TBT_func.case4(distance_matrix, dep_starts, pickups_deliveries, pick_weights, weight_limits))

        if (not all([distance_matrix, dep_starts, pickups_deliveries, pick_weights, weight_limits])):
            js = TBT_func.ErrorGen("TBT Param Error: Missing Param.")
            res = Response(js, status=200, mimetype='application/json')
            return res
            # TODO: Exception Handling
        else:
            # js = TBT_func.case4(distance_matrix, dep_starts, pickups_deliveries, pick_weights, weight_limits)
            # res = Response(js, status=200, mimetype='application/json')
            # return res
            try:
                js = TBT_func.case4(distance_matrix, dep_starts, pickups_deliveries, pick_weights, weight_limits)
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
    try:
        id = request.args.get('id')
        case = request.args.get('case')
        id = int(id)
        case = int(case)
    except:
        js = TBT_func.ErrorGenPreset("TBT Param Error: parameter missing / parameter is not integer.")
        res = Response(js, status=400, mimetype='application/json')
        return res
    else:
        pass

    validId = [0]
    validCase = [[1,2,3,4]]

    if (not int(id) in validId):
        js = TBT_func.ErrorGenPreset("TBT Param Error: ID %d is not in the valid-preset-ID-list." % id)
        res = Response(js, status=400, mimetype='application/json')
        return res
    elif (not int(case) in validCase[int(id)]):
        errortype = "TBT Param Error: case %d is not in the valid-case-list for preset %d." % (case,id)
        js = TBT_func.ErrorGenPreset(errortype)
        res = Response(js, status=400, mimetype='application/json')
        return res
    else:
        js = TBT_preset.preset(id, case)
        res = Response(js, status=200, mimetype='application/json')
        return res

if __name__ == "__main__":
    # app.run(host="0.0.0.0",debug=True,port=2019)
    app.run(debug=True, port=2019)