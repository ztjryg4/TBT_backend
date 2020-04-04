from VRP_P import VRP
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import pandas as pd
import matplotlib.pyplot as plt
import json

def ErrorGen(ErrorType):
    msg = {
                "status": ErrorType,
                "data": {
                    "routes": "",
                    "distance_of_routes": "",
                    "num_vehicles": "",
                    "vehicle_capacities": "",
                }
            }
    js = json.dumps(msg, ensure_ascii=False)
    return js

def ErrorGenPreset(ErrorType):
    msg = {
                "status": ErrorType,
                "data": {
                    }
            }
    js = json.dumps(msg, ensure_ascii=False)
    return js

def case1(distance_matrix, demands, dep_starts, dep_ends, vehicle_capacities):
    '''
    有车子数量以及每辆车的限载的约束时，输入参数为 dep_starts, dep_ends, num_vehicles, vehicle_capacities。
    '''
    # b_loc = pd.read_csv(r'./BasicLocations.csv')
    # b_dist = squareform(pdist(b_loc.values[:, 1:3])).astype(int)
    b_dist = np.array(distance_matrix)
    vrp = VRP(
        distance_matrix=b_dist, demands=demands, dep_starts=dep_starts, dep_ends=dep_ends,
        num_vehicles=len(vehicle_capacities),
        vehicle_capacities=vehicle_capacities,
        travel_time_limit=int(1e9),
        vehicle_speed=int(1e9),
        max_travel_distance=3000
    )
    vrp.solve()
    result = vrp.result()
    msg = {
        "status": "success",
        "data": {
            "routes": result['routes'],
            "distance_of_routes": np.array(result['distance_of_routes']).tolist(),
            "num_vehicles": len(vehicle_capacities),
            "vehicle_capacities": np.array(vehicle_capacities).tolist(),
        }
    }
    js = json.dumps(msg, ensure_ascii=False)
    return js

def case2(distance_matrix, demands, dep_starts, dep_ends, num_vehicles):
    '''
    只给定车子数量，输入参数为 dep_starts, dep_ends, num_vehicles
    '''
    # b_loc = pd.read_csv(r'./BasicLocations.csv')
    # b_dist = squareform(pdist(b_loc.values[:, 1:3])).astype(int)
    b_dist = np.array(distance_matrix)
    vrp = VRP(
        distance_matrix=b_dist, demands=demands, dep_starts=dep_starts, dep_ends=dep_ends,
        num_vehicles=num_vehicles,
        # vehicle_capacities=b_capa,
        travel_time_limit=int(1e9),
        vehicle_speed=int(1e9),
        max_travel_distance=3000
    )
    vrp.solve()
    result = vrp.result()
    # print(result)
    msg = {
        "status": "success",
        "data": {
            "routes": result['routes'],
            "distance_of_routes": np.array(result['distance_of_routes']).tolist(),
            "num_vehicles": num_vehicles,
            "vehicle_capacities": np.array(result['vehicle_capacities']).tolist(),
        }
    }
    js = json.dumps(msg, ensure_ascii=False)
    return js

def case3(distance_matrix, demands, depot, vehicle_capacities):
    '''
    只给定限载的约束，这时，限制为一个配送中心，输入参数为 depot, vehicle_capacities，其中vehicle_capacities 内元素unique
    '''
    # b_loc = pd.read_csv(r'./BasicLocations.csv')
    # b_dist = squareform(pdist(b_loc.values[:, 1:3])).astype(int)
    b_dist = np.array(distance_matrix)
    vrp = VRP(
        distance_matrix=b_dist, demands=demands, depot=depot,
        # num_vehicles=len(b_capa),
        vehicle_capacities=vehicle_capacities,
        travel_time_limit=int(1e9),
        vehicle_speed=int(1e9),
        max_travel_distance=3000
    )
    vrp.solve()
    result = vrp.result()
    print(result['routes'])
    msg = {
        "status": "success",
        "data": {
            "routes": result['routes'],
            "distance_of_routes": np.array(result['distance_of_routes']).tolist(),
            "num_vehicles": len(vehicle_capacities),
            "vehicle_capacities": np.array(vehicle_capacities).tolist(),
        }
    }
    js = json.dumps(msg, ensure_ascii=False)
    return js

def case4(distance_matrix, dep_starts, pickups_deliveries, pick_weights=None, weight_limits=None):
    distance_matrix = np.array(distance_matrix)
    if (pick_weights == None) or (weight_limits == None):
        print("No pick_weights or weight_limits")
        vrp = VRP(
            distance_matrix=distance_matrix, dep_starts=dep_starts, pickups_deliveries=pickups_deliveries,
            num_vehicles=len(dep_starts),
            max_travel_distance=3000
        )
    else:
        print("exist pick_weights or weight_limits")
        vrp = VRP(
            distance_matrix=distance_matrix, dep_starts=dep_starts, pickups_deliveries=pickups_deliveries,
            num_vehicles=len(dep_starts),
            max_travel_distance=3000,
            pick_weights=pick_weights,
            weight_limits=weight_limits
        )
    vrp.solve()
    result = vrp.result_pd()
    # print(result['routes'])
    print(result)
    msg = {
        "status": "success",
        "data": {
            "routes": result['routes'],
            "distance_of_routes": np.array(result['distance_of_routes']).tolist(),
            "num_vehicles": result['num_vehicles'],
            # "vehicle_capacities": np.array(vehicle_capacities).tolist(),
        }
    }
    js = json.dumps(msg, ensure_ascii=False)
    return js

if __name__ == "__main__":

    vehicle_capacities = [14, 14, 16, 16]
    dep_starts = [0, 0, 1, 1]
    dep_ends = dep_starts
    num_vehicles = 4
    distance_matrix = [
        [   0,  392,  557,  515,  417,  196,  377,  139,  241,  139,  462, 377,  278,  265,  331,  557,  468 ],
        [ 392,    0,  684,  241,  139,  377,  592,  265,  515,  526,  792, 493,  480,  571,  722,  679,  857 ],
        [ 557,  684,    0,  915,  802,  377,  196,  618,  331,  526,  400, 931,  835,  799,  604, 1114,  650 ],
        [ 515,  241,  915,    0,  114,  575,  802,  377,  702,  653,  966, 415,  460,  589,  835,  560,  974 ],
        [ 417,  139,  802,  114,    0,  462,  688,  278,  592,  557,  859, 400,  415,  531,  745,  571,  884 ],
        [ 196,  377,  377,  575,  462,    0,  228,  241,  139,  240,  417, 557,  468,  460,  415,  745,  531 ],
        [ 377,  592,  196,  802,  688,  228,    0,  462,  139,  331,  265, 755,  653,  606,  415,  931,  480 ],
        [ 139,  265,  618,  377,  278,  241,  462,    0,  342,  278,  592, 331,  265,  320,  468,  526,  606 ],
        [ 241,  515,  331,  702,  592,  139,  139,  342,    0,  196,  278, 618,  515,  468,  320,  792,  415 ],
        [ 139,  526,  526,  653,  557,  240,  331,  278,  196,    0,  342, 462,  351,  278,  196,  618,  331 ],
        [ 462,  792,  400,  966,  859,  417,  265,  592,  278,  342,    0, 802,  688,  592,  278,  943,  265 ],
        [ 377,  493,  931,  415,  400,  557,  755,  331,  618,  462,  802,   0,  114,  241,  575,  196,  702 ],
        [ 278,  480,  835,  460,  415,  468,  653,  265,  515,  351,  688, 114,    0,  139,  462,  278,  592 ],
        [ 265,  571,  799,  589,  531,  460,  606,  320,  468,  278,  592, 241,  139,    0,  342,  351,  462 ],
        [ 331,  722,  604,  835,  745,  415,  415,  468,  320,  196,  278, 575,  462,  342,    0,  688,  139 ],
        [ 557,  679, 1114,  560,  571,  745,  931,  526,  792,  618,  943, 196,  278,  351,  688,    0,  798 ],
        [ 468,  857,  650,  974,  884,  531,  480,  606,  415,  331,  265, 702,  592,  462,  139,  798,    0 ]
    ]
    demands = [0, 0, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]

    # print(case1(distance_matrix, demands, dep_starts, dep_ends, vehicle_capacities))
    # print(case2(dep_starts, dep_ends, num_vehicles))
    
    # vehicle_capacities = [14, 16]
    # depot = 0
    # print(case3(depot, vehicle_capacities))
    dep_starts = [1, 6]
    pickups_deliveries = [
        [2, 10],
        [4, 3],
        [5, 9],
        [7, 8],
        [15, 11],
        [13, 12],
        [16, 14],
    ]
    pick_weights=1
    weight_limits=[3,3]
    case4(distance_matrix, dep_starts, pickups_deliveries, pick_weights, weight_limits)