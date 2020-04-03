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

def case1(dep_starts, dep_ends, vehicle_capacities):
    '''
    有车子数量以及每辆车的限载的约束时，输入参数为 dep_starts, dep_ends, num_vehicles, vehicle_capacities。
    '''
    b_loc = pd.read_csv(r'./BasicLocations.csv')
    b_dist = squareform(pdist(b_loc.values[:, 1:3])).astype(int)
    
    vrp = VRP(
        distance_matrix=b_dist, demands=b_loc['demand'], dep_starts=dep_starts, dep_ends=dep_ends,
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

def case2(dep_starts, dep_ends, num_vehicles):
    '''
    只给定车子数量，输入参数为 dep_starts, dep_ends, num_vehicles
    '''
    b_loc = pd.read_csv(r'./BasicLocations.csv')
    b_dist = squareform(pdist(b_loc.values[:, 1:3])).astype(int)

    vrp = VRP(
        distance_matrix=b_dist, demands=b_loc['demand'], dep_starts=dep_starts, dep_ends=dep_ends,
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

def case3(depot, vehicle_capacities):
    '''
    只给定限载的约束，这时，限制为一个配送中心，输入参数为 depot, vehicle_capacities，其中vehicle_capacities 内元素unique
    '''
    b_loc = pd.read_csv(r'./BasicLocations.csv')
    b_dist = squareform(pdist(b_loc.values[:, 1:3])).astype(int)

    b_capa = [14, 16]
    vrp = VRP(
        distance_matrix=b_dist, demands=b_loc['demand'], depot=depot,
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

if __name__ == "__main__":

    vehicle_capacities = [14, 14, 16, 16]
    dep_starts = [0, 0, 1, 1]
    dep_ends = dep_starts
    num_vehicles = 4
    
    # print(case1(dep_starts, dep_ends, vehicle_capacities))
    print(case2(dep_starts, dep_ends, num_vehicles))
    
    vehicle_capacities = [14, 16]
    depot = 0
    # print(case3(depot, vehicle_capacities))