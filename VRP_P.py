from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np


class VRP:
    def __init__(
            self, distance_matrix, demands=None, dep_starts=[], dep_ends=[],
            depot=-1, pickups_deliveries=None, num_vehicles=None, vehicle_capacities=None, pick_weights=None,
            weight_limits = None, discharge_time=0, time_limit=20, travel_time_limit=int(1e9), vehicle_speed=int(1e9),
            max_travel_distance=3000, strategy='AUTOMATIC'
    ):
        self.starts = dep_starts
        self.ends = dep_ends
        self.distance_matrix = distance_matrix  # 距离方阵
        self.demands = demands  # 列表 各个配送点的需求，配送点次序应当与distance_matrix保持一致
        self.depot = depot  # 整数 配送中心的下标，默认为0，即distance_matrix中第一个出现的点
        self.time_limit = time_limit  # 整数（秒） 超过这个时间则叫停算法，返回结果
        self.strategy = strategy  # 字符串 指定具体启发式算法 可选：
        self.routes = []
        self.time_matrix = distance_matrix  # 路程时间方阵
        self.travel_time_limit = travel_time_limit
        self.distance_of_routes = []
        self.vehicle_speed = vehicle_speed
        self.discharge_time = discharge_time  # 卸货时间单位/分
        self.max_travel_distance = max_travel_distance
        self.pickups_deliveries = pickups_deliveries  # n*2列表，第一列为取外卖点，第二列为送外卖点。
        self.pick_weights = pick_weights              # int或者list，每一个外卖的重量，当为int时，
                                                      #     表示每个外卖都为这个int值，当为list时，即为
                                                      #     各个外卖的重量，元素个数与上面变量的行数相同，即n
                                                      #     当其值为1时，可以把外卖重量转化为同时携带的外卖数。
        self.weight_limits = weight_limits            # int或者list，每一个外卖员最多同时携带外卖数量，
                                                      #     当为int时，所有外卖员的限制携带外卖数都为这个值
                                                      #     当为list时，即为各个外卖员的携带限制数。此时要满足
                                                      #     len(weight_limits)==num_vehicles
        if pickups_deliveries is not None:
            self.mode = 'PD'
            self.num_vehicles = num_vehicles
        elif num_vehicles is not None and vehicle_capacities is not None:  # 给定车辆数量和车子容量
            if num_vehicles != len(vehicle_capacities):
                raise ValueError('`num_vehicles` must be equal to `len(vehicle_capacities`' \
                                 ' when both provided')
            self.mode = 'BOTH'
            self.num_vehicles = num_vehicles
            self.vehicle_capacities = vehicle_capacities
        elif num_vehicles is not None and vehicle_capacities is None:  # 给定车辆数量，不给定车子容量
            self.mode = 'NONLY'
            self.num_vehicles = num_vehicles
            self.vehicle_capacities = []
        elif num_vehicles is None and vehicle_capacities is not None:  # 不给定车辆数量，给定车子容量
            if len(vehicle_capacities) != len(set(vehicle_capacities)):
                raise ValueError('`vehicle_capacities` must contain unique numbers ' \
                                 ' when `num_vehicles` is not provided')
            self.mode = 'CONLY'
            self.capacity_options = vehicle_capacities
            self.num_vehicles = None
            self.vehicle_capacities = vehicle_capacities
        else:  # 二者都不给定
            self.mode = 'NONE'
            self.num_vehicles = len(distance_matrix) // 5
            # self.num_vehicles = 2
            self.vehicle_capacities = None

    def solve(self):
        if self.mode == 'BOTH':
            self._solve_vrp_with_capacity_constraint()
        elif self.mode == 'CONLY':
            capacity_options = self.vehicle_capacities
            max_capacity = max(self.vehicle_capacities)
            self.num_vehicles = int(np.ceil(np.sum(self.demands) / max_capacity))  # ceil a = [x] + 1
            self.vehicle_capacities = self.num_vehicles * [max_capacity]
            self._solve_vrp_with_capacity_constraint()
            self._sum_demands()
            self.vehicle_capacities = np.array(self.vehicle_capacities)
            self.capacity_options = sorted(self.capacity_options)
            self.vehicle_capacities[self.vehicle_capacities <= capacity_options[0]] = capacity_options[0]
            for i in range(1, len(self.capacity_options)):
                bound1 = capacity_options[i - 1] < self.vehicle_capacities
                bound2 = self.vehicle_capacities <= capacity_options[i]
                bound = bound1 & bound2
                self.vehicle_capacities[bound] = capacity_options[i]
            self.vehicle_capacities = self.vehicle_capacities.tolist()
        elif self.mode == 'PD':
            self._solve_vrp_with_pickups_deliveries()
        else:
            self._solve_classic_vrp()
            self._sum_demands()

    def result(self):
        return {
            'distance_matrix': self.distance_matrix,
            'demands': self.demands,
            'starts': self.starts,
            'num_vehicles': self.num_vehicles,
            'vehicle_capacities': self.vehicle_capacities,
            'routes': self.routes,
            'distance_of_routes': self.distance_of_routes,
        }

    def result_pd(self):
        return {
            'routes': self.routes,
            'distance_of_routes':self.distance_of_routes,
            'starts':self.starts,
            'num_vehicles':self.num_vehicles,
            'weight_limits':self.weight_limits,
            'pick_weights':self.pick_weights
        }

    def _solve_vrp_with_pickups_deliveries(self):
        # 在距离矩阵上方扩充一行零矩阵，左方扩充一列零矩阵，使得形状由N*N变为(N+1)*(N+1)
        self.distance_matrix = np.c_[np.zeros(self.distance_matrix.shape[0], dtype=int), self.distance_matrix]
        self.distance_matrix = np.row_stack((np.zeros(self.distance_matrix.shape[1], dtype=int), self.distance_matrix))

        manager = pywrapcp.RoutingIndexManager(
            len(self.distance_matrix),
            self.num_vehicles,
            self.starts,
            [0] * self.num_vehicles,
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        if self.pick_weights and self.weight_limits:
            pickups_deliveries = np.array(self.pickups_deliveries).T
            if isinstance(self.pick_weights, int):
                pick_weights = [self.pick_weights] * pickups_deliveries.shape[1]
            else:
                pick_weights = self.pick_weights
            # print(pick_capacities)
            # print(self.pickups_deliveries.shape)
            # print(self.pickups_deliveries)
            self.pick_weights = pick_weights
            pick_weights = [0] * len(self.distance_matrix)
            for i in range(2):
                for j in range(pickups_deliveries.shape[1]):
                    pick_weights[pickups_deliveries[i][j]] = pick_weights[j] * (-2 * i + 1)
            # print(pick_weights)

            def weight_callback(from_index):
                from_node = manager.IndexToNode(from_index)
                return pick_weights[from_node]
            if isinstance(self.weight_limits, int):
                weight_limits = [self.weight_limits] * self.num_vehicles
            else:
                weight_limits = self.weight_limits
            self.weight_limits = weight_limits
            weight_callback_index = routing.RegisterUnaryTransitCallback(weight_callback)
            routing.AddDimensionWithVehicleCapacity(
                weight_callback_index,
                0,
                weight_limits,
                True,
                'Weight'
            )

        for request in self.pickups_deliveries:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(
                    delivery_index))
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index) <=
                distance_dimension.CumulVar(delivery_index))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
        search_parameters.time_limit.seconds = 2
        # search_parameters.log_search = True

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            # print_solution(data, manager, routing, solution)
            for route_nbr in range(self.num_vehicles):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]
                # print('route:', route)
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                self.routes.append(route)

            for i in range(len(self.routes)):
                self.routes[i] = self.routes[i][:-1]
            # print(self.routes)
        self._distance_routes()
        # print(self.distance_of_routes)

    def _solve_classic_vrp(self):
        if self.depot == -1:
            manager = pywrapcp.RoutingIndexManager(
                len(self.distance_matrix),
                self.num_vehicles,
                self.starts,
                self.ends
            )
        else:
            manager = pywrapcp.RoutingIndexManager(
                len(self.distance_matrix),
                self.num_vehicles,
                self.depot,
            )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        def time_callback(from_index, to_index):
            from_note = manager.IndexToNode(from_index)
            to_note = manager.IndexToNode(to_index)
            return self.time_matrix[from_note][to_note] + self.discharge_time * self.vehicle_speed

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,
            self.max_travel_distance,
            True,
            dimension_name)
        # distance_dimension = routing.GetDimensionOrDie(dimension_name)
        # distance_dimension.SetGlobalSpanCostCoefficient(100)

        time_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.AddDimension(
            time_callback_index,
            0,
            self.travel_time_limit * self.vehicle_speed,
            True,
            'Time'
        )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.time_limit.seconds = self.time_limit
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

        search_parameters.local_search_metaheuristic = \
            (routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
        search_parameters.time_limit.seconds = 2
        # search_parameters.log_search = True

        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            self.routes = []
            for route_nbr in range(self.num_vehicles):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                self.routes.append(route)
        self._distance_routes()

    def _solve_vrp_with_capacity_constraint(self):
        if self.depot == -1:
            manager = pywrapcp.RoutingIndexManager(
                len(self.distance_matrix),
                self.num_vehicles,
                self.starts,
                self.ends
            )
        else:
            manager = pywrapcp.RoutingIndexManager(
                len(self.distance_matrix),
                self.num_vehicles,
                self.depot,
            )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        def time_callback(from_index, to_index):
            from_note = manager.IndexToNode(from_index)
            to_note = manager.IndexToNode(to_index)
            return self.time_matrix[from_note][to_note] + self.discharge_time * self.vehicle_speed

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return self.demands[from_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.AddDimension(
            transit_callback_index,
            0,
            self.max_travel_distance,
            True,
            'Distance'
        )
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            self.vehicle_capacities,
            True,
            'Capacity'
        )

        time_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.AddDimension(
            time_callback_index,
            0,
            self.travel_time_limit * self.vehicle_speed,
            True,
            'Time'
        )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.time_limit.seconds = self.time_limit
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

        search_parameters.local_search_metaheuristic = \
            (routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
        search_parameters.time_limit.seconds = 2
        # search_parameters.log_search = True

        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            self.routes = []
            for route_nbr in range(self.num_vehicles):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                self.routes.append(route)
        self._distance_routes()

    def _sum_demands(self):
        self.vehicle_capacities = []
        for route in self.routes:
            capacity = 0
            for point in route:
                capacity += self.demands[point]
            self.vehicle_capacities.append(capacity)

    def _distance_routes(self):
        # print(np.array(self.distance_matrix))
        for route in self.routes:
            distance = 0
            for i in range(len(route) - 1):
                distance += self.distance_matrix[route[i]][route[i + 1]]
                # print(route[i], route[i + 1], self.distance_matrix[route[i]][route[i + 1]])
            self.distance_of_routes.append(distance)