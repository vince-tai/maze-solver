import time, random

from cell import Cell

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            self._cells.append([])
            for _ in range(self._num_rows):
                self._cells[i].append(Cell(self._win))
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cells(i, j)
    
    def _draw_cells(self, i, j):
        if self._win is None:
            return
        self._cells[i][j]._x1 = self._x1 + (self._cell_size_x * i)
        self._cells[i][j]._y1 = self._y1 + (self._cell_size_y * j)
        self._cells[i][j]._x2 = self._cells[i][j]._x1 + self._cell_size_x
        self._cells[i][j]._y2 = self._cells[i][j]._y1 + self._cell_size_y
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cells(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cells(self._num_cols - 1, self._num_rows - 1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            to_visit = []
            if i < self._num_cols - 1 and not self._cells[i + 1][j]._visited:
                to_visit.append("right")
            if i >= 1 and not self._cells[i - 1][j]._visited:
                to_visit.append("left")
            if j >= 1 and not self._cells[i][j - 1]._visited:
                to_visit.append("top")
            if j < self._num_rows - 1 and not self._cells[i][j + 1]._visited:
                to_visit.append("bottom")
            if to_visit == []:
                self._cells[i][j].draw()
                return
            
            direction = to_visit[random.randrange(len(to_visit))]
            match direction:
                case "right":
                    self._cells[i][j].has_right_wall = False
                    self._cells[i + 1][j].has_left_wall = False
                    self._break_walls_r(i + 1, j)
                case "left":
                    self._cells[i][j].has_left_wall = False
                    self._cells[i - 1][j].has_right_wall = False
                    self._break_walls_r(i - 1, j)
                case "top":
                    self._cells[i][j].has_top_wall = False
                    self._cells[i][j - 1].has_bottom_wall = False
                    self._break_walls_r(i, j - 1)
                case "bottom":
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i][j + 1].has_top_wall = False
                    self._break_walls_r(i, j + 1)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j]._visited = False

        
