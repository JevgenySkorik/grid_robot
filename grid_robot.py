import serial
import time
import collections


arduino = serial.Serial('COM14', baudrate=9600) # Same baudrate, as in Arduino program
time.sleep(2)
wall, clear, goal = "#", ".", "*"
grid = ["........",
        "...#...#",
        "..##...#",
        ".....###",
        "........",
        "...#...#",
        "..##...#",
        "........"]
width, height = len(grid[0]), len(grid)
stack = []
obstacles = []
explored_cells = []
current_position = (0, 0)
#   w
# a . d     starting orientation of the robot relative to the grid
#   s
orientation = 'w'

# Function for changing char in string
def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])


# Stack based flood fill grid exploration algorithm
def flood_fill(x, y):
    global current_position
    explore_cell(x, y)
    print(stack)
    
    i = 1
    while (stack):
        print(f"\n{i} iteration")
        print(f"orientation: {orientation}")
        print(f"current position: {current_position}")
        print(f"stack: {stack}")
        print(f"obstacles: {obstacles}")
        print(f"explored_cells: {sorted(explored_cells)} {len(explored_cells)}")
        i += 1
        

        to_explore = stack.pop()
        actions = explore_cell(to_explore[0], to_explore[1])
        current_position = (to_explore[0], to_explore[1])
        if i == 15: return

def explore_cell(x, y):
    if (not already_explored(x, y)):    explore(x, y)

    if (not already_explored(x, y-1)):  stack.append((x, y-1))
    if (not already_explored(x+1, y)):  stack.append((x+1, y))
    if (not already_explored(x, y+1)):  stack.append((x, y+1))
    if (not already_explored(x-1, y)):  stack.append((x-1, y))


def explore(x, y):
    print(f"exploring({x}, {y})")
    # Get to cell
    path = bfs(grid, current_position, (x, y))
    actions = path_to_actions(path)
    print(f"path: {path}")
    print(f"actions: {actions}")
    # Mark cell as explored
    grid[y] = replace_str_index(grid[y], x, ',')
    explored_cells.append((x, y))
    print_grid()


def already_explored(x, y):
    global current_position
    # If point outside of grid or current point, dont explore
    if not 0 <= y < len(grid) or not 0 <= x < len(grid[y]) or current_position == (x, y):
        return True
    # If cell is already explored or is known obstacle, dont explore
    if ((x, y) in explored_cells or (x, y) in obstacles):
        return True
    # Check if cell is an obstacle
    print(f"explore obstacle at ({x}, {y})")
    obstacle_check = action_to_obstacle_check(path_to_actions([current_position, (x, y)])[0])
    print(f"obstacle check: {obstacle_check}")
    if (grid[y][x] == '#'):
        print(f"obstacle found at ({x}, {y})!")
        if ((x, y) not in obstacles): obstacles.append((x, y))
        return True
    return False


# Solve grid
def bfs(grid, start, finish):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == finish:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

 
# Returns actions to perform to traverse path
def path_to_actions(path):
    global orientation
    # If path is to same cell, skip
    try:
        if (path[0] == path[-1]):
            return None
    except:
        pass

    actions = []
    for i in range(len(path) - 1):
        correct_orientation = ' '
        current_pos = path[i]
        new_pos = path[i+1]
        dx = current_pos[0] - new_pos[0]
        dy = current_pos[1] - new_pos[1]
 
        # find correct orientation
        if   (dx == -1):    correct_orientation = 'd'
        elif (dx == 1):     correct_orientation = 'a'
        elif (dy == -1):    correct_orientation = 's'
        elif (dy == 1):     correct_orientation = 'w'
        else:   correct_orientation = orientation
 
        # align robot
        if (orientation == 'w'):
            if (correct_orientation == 'a'):    actions.append("turn_left")
            if (correct_orientation == 'd'):    actions.append("turn_right")
            if (correct_orientation == 's'):    actions.append("u-turn")
        if (orientation == 'a'):
            if (correct_orientation == 'w'):    actions.append("turn_right")
            if (correct_orientation == 'd'):    actions.append("u-turn")
            if (correct_orientation == 's'):    actions.append("turn_left")
        if (orientation == 'd'):
            if (correct_orientation == 'w'):    actions.append("turn_left")
            if (correct_orientation == 'a'):    actions.append("u-turn")
            if (correct_orientation == 's'):    actions.append("turn_right")
        if (orientation == 's'):
            if (correct_orientation == 'w'):    actions.append("u-turn")
            if (correct_orientation == 'a'):    actions.append("turn_right")
            if (correct_orientation == 'd'):    actions.append("turn_left")
        orientation = correct_orientation
        actions.append("go_forward")
 
    return actions

def action_to_obstacle_check(action):
    obstacle_check = []
    if (action != "go_forward"):
        obstacle_check.append(action)

    obstacle_check.append("check_obstacle")
    return obstacle_check

def print_grid():
    for line in grid:
        print(line)


# Prints solved maze('@' is start, '*' is finish) 
def print_solved_path(grid, start, path):
    solved_grid = grid
    for point in path:
        # skip last point
        if point == path[-1]: break
        # mark path
        solved_grid[point[1]] = solved_grid[point[1]][:point[0]] + "o" + solved_grid[point[1]][point[0]+1:]
 
    # mark start
    solved_grid[start[1]] = solved_grid[start[1]][:start[0]] + "@" + solved_grid[start[1]][start[0]+1:]
    for line in solved_grid:
        print(line)


# Main loop(solve and traverse a maze)
def main():
    flood_fill(current_position[0], current_position[1])
    # Solve grid
    # path = bfs(grid, start)
    # print("Solved path:")
    # print_solved_path(grid, start, path)
    # print(path)

    # Get actions needed to traverse path
    # actions = path_to_actions(path)

    # Perform the actions
    # print(f"Actions:\n{actions}")
    # for action in actions:
    #     if      action == "go_forward":    print(action)#arduino.write(bytes("FC", 'utf-8'))
    #     elif    action == "turn_left":     print(action)#arduino.write(bytes("L", 'utf-8'))
    #     elif    action == "turn_right":    print(action)#arduino.write(bytes("R ", 'utf-8'))
    #     elif    action == "u-turn":        print(action)#arduino.write(bytes("RR", 'utf-8'))


# Function for testing robot
def test():
    arduino.write(bytes("F", 'utf-8'))
    # arduino.write(bytes("L", 'utf-8'))
    # arduino.write(bytes("R ", 'utf-8'))
    # arduino.write(bytes("RR", 'utf-8'))
    # arduino.write(bytes("FC", 'utf-8'))


# Uncomment "test()" when testing, "main()" when launching main program
if __name__ == "__main__":
    main()
    #test()
