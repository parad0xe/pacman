from src.models.direction import Direction

from heapq import heappush, heappop

class PathFinder():
    def __init__(self, maze: list[list[int]] = []) -> None:
        self.maze = maze

    def new_maze(self, maze: list[list[int]]) -> None:
        """
        changes the class maze when the level changes
        """
        self.maze = maze

    @staticmethod
    def dist(src: tuple[int, int], dest: tuple[int, int]) -> int:
        """
        calculates the manathan distance between two nodes
        """
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

    def neighbors(self, pos: tuple[int, int]) \
            -> list[tuple[int, int]]:
        """
        return the coordinate of the avaible neighbors from 'pos' cell
        """
        neighbors_coords: list[tuple[int, int]] = []
        walls: int = self.maze[pos[1]][pos[0]]

        if not walls & 1:
            neighbors_coords.append((pos[0], pos[1] - 1))
        if not walls & 2:
            neighbors_coords.append((pos[0] + 1, pos[1]))
        if not walls & 4:
            neighbors_coords.append((pos[0], pos[1] + 1))
        if not walls & 8:
            neighbors_coords.append((pos[0] - 1, pos[1]))
        return neighbors_coords

    def dir(self, src: tuple[int, int], dest: tuple[int, int]) -> Direction:
        if dest[0] - src[0] == 1:
            return Direction.EAST
        if dest[0] - src[0] == -1:
            return Direction.WEST
        if dest[1] - src[1] == 1:
            return Direction.SOUTH
        if dest[1] - src[1] == -1:
            return Direction.NORTH
        return Direction.IDLE

    def reconstruct(self, came_from: dict,
                    start: tuple[int, int],
                    end: tuple[int, int]) -> list[Direction]:
        path: list[Direction] = []
        cur = end
        while cur != start:
            prev = came_from[cur]
            path.append(self.dir(prev, cur))
            cur = prev
        path.reverse()
        return path

    def search(self, start: tuple[int, int], end: tuple[int, int])\
    -> list[Direction]:
        open_heap: list[tuple[int, int, tuple[int, int]]] = []
        heappush(open_heap, (self.dist(start, end), 0, start))

        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g: dict[tuple[int, int], int] = {start: 0}
        closed: set[tuple[int, int]] = set()

        while open_heap:
            _, g_cur, cur = heappop(open_heap)

            if cur == end:
                return self.reconstruct(came_from, start, end)

            if cur in closed:
                continue
            closed.add(cur)

            for neighbor in self.neighbors(cur):
                if neighbor in closed:
                    continue
                g_new = g_cur + 1
                if g_new < g.get(neighbor, float('inf')):
                    g[neighbor] = g_new
                    f_new = g_new + self.dist(neighbor, end)
                    came_from[neighbor] = cur
                    heappush(open_heap, (f_new, g_new, neighbor))
        return []
