import json
import TBT_func

validId = [0]
validCase = [[1,2,3,4]]
loc = []
distance_matrix = []

loc.append([{"name":"P","x":"456","y":"320","demand":"0"},
            {"name":"A","x":"228","y":"0","demand":"0"},
            {"name":"B","x":"912","y":"0","demand":"1"},
            {"name":"C","x":"0","y":"80","demand":"2"},
            {"name":"D","x":"114","y":"80","demand":"4"},
            {"name":"E","x":"570","y":"160","demand":"2"},
            {"name":"F","x":"798","y":"160","demand":"4"},
            {"name":"G","x":"342","y":"240","demand":"8"},
            {"name":"H","x":"684","y":"240","demand":"8"},
            {"name":"I","x":"570","y":"400","demand":"1"},
            {"name":"J","x":"912","y":"400","demand":"2"},
            {"name":"K","x":"114","y":"480","demand":"1"},
            {"name":"L","x":"228","y":"480","demand":"2"},
            {"name":"M","x":"342","y":"560","demand":"4"},
            {"name":"N","x":"684","y":"560","demand":"4"},
            {"name":"O","x":"0","y":"640","demand":"8"},
            {"name":"P","x":"798","y":"640","demand":"8"}
        ])

distance_matrix.append([[   0,  392,  557,  515,  417,  196,  377,  139,  241,  139,  462, 377,  278,  265,  331,  557,  468 ],
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
                        [ 468,  857,  650,  974,  884,  531,  480,  606,  415,  331,  265, 702,  592,  462,  139,  798,    0 ]])

def preset(id,case):
    id = int(id)
    case = int(case)
    if id == 0:
        msg = ''
        if case == 1:
            msg = {
                "status": "success",
                "data": {
                    "loc" : loc[0],
                    "mode": "both",
                    "distance_matrix": distance_matrix[0],
                    "dep_starts": [0, 0, 1, 1],
                    "dep_ends": [0, 0, 1, 1],
                    "num_vehicles": 4,
                    "vehicle_capacities": [14, 14, 16, 16],
                    "demands": [0, 0, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
                }
            }
        elif case == 2:
            msg = {
                "status": "success",
                "data": {
                    "loc" : loc[0],
                    "mode": "num",
                    "distance_matrix": distance_matrix[0],
                    "dep_starts": [0, 0, 1, 1],
                    "dep_ends": [0, 0, 1, 1],
                    "num_vehicles": 4,
                    "vehicle_capacities": [14, 14, 16, 16],
                    "demands": [0, 0, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
                }
            }
        elif case == 3:
            msg = {
                "status": "success",
                "data": {
                    "loc" : loc[0],
                    "mode": "cap",
                    "distance_matrix": distance_matrix[0],
                    "dep_starts": [1, 6],
                    "num_vehicles": 4,
                    "vehicle_capacities": [14, 16],
                    "demands": [0, 0, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
                }
            }
        elif case == 4:
            msg = {
                "status": "success",
                "data": {
                    "loc" : loc[0],
                    "mode": "takeaway",
                    "distance_matrix": distance_matrix[0],
                    "dep_starts":[1, 6],
                    "pickups_deliveries" : [[2, 10],
                                            [4, 3],
                                            [5, 9],
                                            [7, 8],
                                            [15, 11],
                                            [13, 12],
                                            [16, 14]],
                    "pick_weights": 1,
                    "weight_limits": [3, 3]
                }
            }
        js = json.dumps(msg, ensure_ascii=False)
        return js

if __name__ == "__main__":
    print(preset(0,4))