class Map:
    def __init__(self, value_map, closed_map, parents_map, cost_map, road_map):
        self.value_map = value_map
        self.closed_map = closed_map
        self.parents_map = parents_map
        self.cost_map = cost_map
        self.road_map = road_map

    def change_five(self):
        for i in range(len(self.cost_map)):
            for j in range(len(self.cost_map)):
                if self.cost_map[i][j] == 5:
                    self.cost_map[i][j] = -5
                    self.value_map[i][j] = -5
                    self.closed_map[i][j] = -5
                    self.parents_map[i][j] = -5
