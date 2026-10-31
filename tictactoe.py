import turtle

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 3
CELL = WIDTH // GRID_SIZE

screen = turtle.Screen()
screen.title("Tic-Tac-Toe")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = "X"
game_over = False

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()


def draw_grid():
    pen.clear()
    for i in range(1, GRID_SIZE):
        x = -WIDTH // 2 + i * CELL
        pen.penup()
        pen.goto(x, -HEIGHT // 2)
        pen.pendown()
        pen.goto(x, HEIGHT // 2)

        y = -HEIGHT // 2 + i * CELL
        pen.penup()
        pen.goto(-WIDTH // 2, y)
        pen.pendown()
        pen.goto(WIDTH // 2, y)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = board[row][col]
            if value == "":
                continue
            x = -WIDTH // 2 + col * CELL + CELL / 2
            y = -HEIGHT // 2 + row * CELL + CELL / 2
            pen.penup()
            pen.goto(x, y - 24)
            pen.write(value, align="center", font=("Courier", 52, "normal"))


def available_moves():
    moves = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "":
                moves.append((row, col))
    return moves


def check_winner():
    lines = []
    for i in range(GRID_SIZE):
        lines.append([(i, 0), (i, 1), (i, 2)])
        lines.append([(0, i), (1, i), (2, i)])
    lines.append([(0, 0), (1, 1), (2, 2)])
    lines.append([(0, 2), (1, 1), (2, 0)])

    for line in lines:
        values = [board[r][c] for r, c in line]
        if values[0] != "" and values[0] == values[1] == values[2]:
            return values[0]
    return None


def reset_board():
    global board, current_player, game_over
    board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"
    game_over = False
    draw_grid()
    pen.goto(0, HEIGHT / 2 - 40)
    pen.color("white")
    pen.write("Player X's turn", align="center", font=("Courier", 18, "normal"))


def handle_click(x, y):
    global current_player, game_over

    if game_over:
        return

    row = int((y + HEIGHT / 2) // CELL)
    col = int((x + WIDTH / 2) // CELL)

    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
        return
    if board[row][col] != "":
        return

    board[row][col] = current_player
    draw_grid()

    winner = check_winner()
    if winner:
        game_over = True
        pen.goto(0, -HEIGHT / 2 + 40)
        pen.clear()
        pen.write(f"Player {winner} wins! Press R to restart", align="center", font=("Courier", 18, "normal"))
        return

    if not available_moves():
        game_over = True
        pen.goto(0, -HEIGHT / 2 + 40)
        pen.clear()
        pen.write("Draw! Press R to restart", align="center", font=("Courier", 18, "normal"))
        return

    current_player = "O" if current_player == "X" else "X"
    pen.goto(0, HEIGHT / 2 - 40)
    pen.clear()
    pen.write(f"Player {current_player}'s turn", align="center", font=("Courier", 18, "normal"))


def restart_game():
    reset_board()


screen.onclick(handle_click)
screen.onkeypress(restart_game, "r")
screen.listen()

reset_board()

while True:
    screen.update()
