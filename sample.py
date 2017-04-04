class Tile:
    # x - columns
    # y - rows
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.neighbours = []
        self.is_free = True

    def __repr__(self):
        return "Tile: %s; %s" % (str(self.y), str(self.x))

    # First initialize the field, only after use this method
    def set_neighbours(self, field):
        if self.y - 1 >= 0:
            self.neighbours.append(field[self.y - 1][self.x])
        if self.y + 1 <= 8:
            self.neighbours.append(field[self.y + 1][self.x])
        if self.x - 1 >= 0:
            self.neighbours.append(field[self.y][self.x - 1])
        if self.x + 1 <= 8:
            self.neighbours.append(field[self.y][self.x + 1])

    def get_position(self):
        return self.y, self.x


class Player:
    # Player number is either 1 or 2
    def __init__(self, player_num, field):
        self.player_name = "Player" + str(player_num)
        self.field = field  # player should know how to field looks like
        if player_num == 1:
            self.y = 0
            self.x = 4
            self.goal = self.field.field[8]
        else:
            self.y = 8
            self.x = 4
            self.goal = self.field.field[0]
        self.number_of_walls = 10
        self.current_tile = self.field.get_tile(self.y, self.x)
        self.current_tile.is_free = False
        self.allowed_tiles = self.show_allowed_moves()
        self.is_winner = False
        self.victim = None

    def set_position(self, y, x):
        self.y = y
        self.x = x

    def set_victim(self, player):
        self.victim = player

    def show_allowed_moves(self):
        allowed_tiles = []
        for i in self.current_tile.neighbours:
            if not i.is_free:
                allowed_tiles += i.neighbours
                allowed_tiles.remove(self.current_tile)
            else:
                allowed_tiles.append(i)
        return allowed_tiles

    def backtrace(self, parent, start, end):
        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()
        path = [x for x in path if x.is_free]
        return path

    def bfs(self, start):
        parent = {}
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node in self.goal:
                return self.backtrace(parent, start, node)
            for neighbour in node.neighbours:
                parent[neighbour] = node
                queue.append(neighbour)

    # def shortest_path(self, tile):
    #     for goal in self.goal:
    #         paths = self.bfs(tile, goal)
    #     shortest_path = []
    #     min_length = None
    #     for path in paths:
    #         if min_length is None:
    #             min_length = len(path)
    #             shortest_path = path
    #         if len(path) < min_length:
    #             min_length = len(path)
    #             shortest_path = path
    #     return shortest_path

    # Receive a tile where to step
    # Should change a tile.is_free field to False
    def move(self, tile):
        self.allowed_tiles = self.show_allowed_moves()
        if tile not in self.allowed_tiles:
            print("You cannot go here!")
        else:
            if tile.is_free:
                self.current_tile.is_free = True
                self.current_tile = tile
                self.set_position(tile.y, tile.x)
                tile.is_free = False
                print(self.player_name + " current position is %s; %s" % (self.y, self.x))
                if self.current_tile in self.goal:
                    self.is_winner = True
                    print(self.player_name + " won the game!")
            else:
                print("You cannot go here!")

    # Tiles position in tiles of type 'hor' goes like this:
    # For example:
    # A B
    # ---
    # C D
    # so the pairs are (A, C) and (B, D)
    # Tiles position in tiles of type 'ver' goes like this:
    # A|C
    #  |
    # B|D
    # so the pairs are (A, C) and (B, D)
    # layout - type of the wall, either horizontal or vertical (hor/ver)
    # returns 1 in success and -1 otherwise
    def place_wall(self, tiles, layout):
        if self.number_of_walls > 0:
            try:
                if layout == 'hor':
                    # Check if walls will not create a cross
                    if str(tiles[0]) + " " + str(tiles[1]) + " " + str(tiles[2]) + " " \
                            + str(tiles[3]) in self.field.walls:
                        raise ValueError
                        # Check if one pair is not a start of another
                    else:
                        if str(tiles[0]) + " " + str(tiles[2]) in self.field.wall_pairs \
                                or str(tiles[1]) + " " + str(tiles[3]) in self.field.wall_pairs:
                            raise ValueError
                        else:
                            tiles[0].neighbours.remove(tiles[2])  # Tile 1 now do not have path to tile 3
                            tiles[2].neighbours.remove(tiles[0])  # The same for tile 3
                            tiles[1].neighbours.remove(tiles[3])  # Tile 2 not do not have path to tile 4
                            tiles[3].neighbours.remove(tiles[1])  # The same for tile 4
                            self.field.wall_pairs.add(str(tiles[0]) + " " + str(tiles[2]))
                            self.field.wall_pairs.add(str(tiles[1]) + " " + str(tiles[3]))
                            self.field.walls.add(
                                str(tiles[0]) + " " + str(tiles[2]) + " "
                                + str(tiles[1]) + " " + str(tiles[3]))
                elif layout == 'ver':
                    # Check if walls will not create a cross
                    if str(tiles[0]) + " " + str(tiles[2]) + " " + str(tiles[1]) + " " \
                            + str(tiles[3]) in self.field.walls:
                        raise ValueError
                    else:
                        # Check if one pair is not start of another
                        if str(tiles[0]) + " " + str(tiles[1]) in self.field.wall_pairs \
                                or str(tiles[2]) + " " + str(tiles[3]) in self.field.wall_pairs:
                            raise ValueError
                        else:
                            tiles[0].neighbours.remove(tiles[1])  # Tile 1 now do not have path to tile 2
                            tiles[1].neighbours.remove(tiles[0])  # The same for tile 2
                            tiles[2].neighbours.remove(tiles[3])  # Tile 3 now do not have path to tile 4
                            tiles[3].neighbours.remove(tiles[2])  # The same for tile 4
                            self.field.wall_pairs.add(str(tiles[0]) + " " + str(tiles[1]))
                            self.field.wall_pairs.add(str(tiles[2]) + " " + str(tiles[3]))
                            self.field.walls.add(
                                str(tiles[0]) + " " + str(tiles[1]) + " "
                                + str(tiles[2]) + " " + str(tiles[3]))
                print("The wall has been placed.")
                self.number_of_walls -= 1
                return 1
            except ValueError:
                print("You cannot place wall here!")
                return -1
        else:
            print("Oops, looks like you do not have walls left!")
            return -1


class Board:
    def __init__(self):
        self.field = [[Tile(i, j) for j in range(9)] for i in range(9)]  # i - rows, j - columns
        self.set_tile_neighbours()
        self.wall_pairs = set()
        self.walls = set()

    def set_tile_neighbours(self):
        for row in self.field:
            for tile in row:
                tile.set_neighbours(self.field)

    def get_tile(self, row, column):
        return self.field[row][column]

# TESTING
board = Board()
# Checking board consistency
for i in board.field:
    print(i)

print("\n")
# Checking neighbours
for i in board.field:
    for j in i:
        print(j)
        print(j.neighbours)

player1 = Player(1, board)
player2 = Player(2, board)

# Checking wall placing
player1.place_wall([board.field[0][0], board.field[0][1], board.field[1][0], board.field[1][1]], "hor")
print("\n")
for i in board.field:
    for j in i:
        print(j)
        print(j.neighbours)

player2.place_wall([board.field[0][2], board.field[0][3], board.field[1][2], board.field[1][3]], "hor")

player1.place_wall([board.field[0][1], board.field[0][2], board.field[1][1], board.field[1][2]], "ver")

player1.move(board.field[1][4])
player2.move(board.field[7][4])
player1.move(board.field[2][4])
player2.move(board.field[6][4])
player1.move(board.field[3][4])
player2.move(board.field[5][4])
player1.move(board.field[4][4])
# player2.move(board.field[3][4])
# player1.move(board.field[5][4])
# player2.move(board.field[2][4])
# player1.move(board.field[6][4])
# player2.move(board.field[1][4])
# player1.move(board.field[7][4])
# player2.move(board.field[0][4])

path = player2.bfs(player2.current_tile)
print(path)
