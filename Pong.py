import random
import turtle

WIDTH = 800
HEIGHT = 600
PADDLE_HEIGHT = 100
PADDLE_SPEED = 28
WIN_SCORE = 5
INITIAL_BALL_SPEED = 0.38
MAX_BALL_SPEED = 2.0

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)


class Paddle:
    def __init__(self, x, y, color="white"):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.shape("square")
        self.t.color(color)
        self.t.shapesize(stretch_wid=5, stretch_len=1)
        self.t.penup()
        self.t.goto(x, y)

    def move_up(self, amount=PADDLE_SPEED):
        y = self.t.ycor() + amount
        self.t.sety(min(y, HEIGHT / 2 - 40))

    def move_down(self, amount=PADDLE_SPEED):
        y = self.t.ycor() - amount
        self.t.sety(max(y, -(HEIGHT / 2 - 40)))

    @property
    def xcor(self):
        return self.t.xcor()

    @property
    def ycor(self):
        return self.t.ycor()


class Ball:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.shape("square")
        self.t.color("white")
        self.t.penup()
        self.goto_center()
        self.dx = 0
        self.dy = 0

    def goto_center(self):
        self.t.goto(0, 0)

    def serve(self, direction):
        self.goto_center()
        self.dx = direction * INITIAL_BALL_SPEED
        self.dy = random.uniform(-INITIAL_BALL_SPEED, INITIAL_BALL_SPEED)

    def move(self):
        self.t.setx(self.t.xcor() + self.dx)
        self.t.sety(self.t.ycor() + self.dy)

    @property
    def xcor(self):
        return self.t.xcor()

    @property
    def ycor(self):
        return self.t.ycor()

    def setx(self, value):
        self.t.setx(value)

    def sety(self, value):
        self.t.sety(value)


paddle_a = Paddle(-350, 0)
paddle_b = Paddle(350, 0)
ball = Ball()

score_a = 0
score_b = 0
state = "ready"

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)

status_pen = turtle.Turtle()
status_pen.speed(0)
status_pen.color("white")
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, -260)


def draw_score():
    score_pen.clear()
    score_pen.write(
        f"Player 1: {score_a}   Player 2: {score_b}",
        align="center",
        font=("Courier", 22, "normal"),
    )


def show_status(message):
    status_pen.clear()
    status_pen.write(message, align="center", font=("Courier", 18, "normal"))


def reset_round(direction):
    global state
    ball.serve(direction)
    if state == "ready":
        state = "playing"
        status_pen.clear()


def start_game():
    global state
    if state == "ready":
        state = "playing"
        status_pen.clear()
        ball.serve(1)
    elif state == "paused":
        state = "playing"
        status_pen.clear()
    elif state == "game_over":
        restart_game()


def toggle_pause():
    global state
    if state == "playing":
        state = "paused"
        show_status("Paused - Press P to resume")
    elif state == "paused":
        state = "playing"
        status_pen.clear()


def restart_game():
    global score_a, score_b, state
    score_a = 0
    score_b = 0
    draw_score()
    paddle_a.t.goto(-350, 0)
    paddle_b.t.goto(350, 0)
    state = "ready"
    ball.serve(1)
    show_status("Press Space to start")


def end_game(winner):
    global state
    state = "game_over"
    show_status(f"{winner} wins! Press R to restart")


def bounce_paddle(paddle, direction):
    relative = (ball.ycor - paddle.ycor) / (PADDLE_HEIGHT / 2)
    ball.dy = relative * 1.8
    ball.dx = direction * min(abs(ball.dx) * 1.08, MAX_BALL_SPEED)


def paddle_a_up():
    if state in ("playing", "ready", "paused"):
        paddle_a.move_up()


def paddle_a_down():
    if state in ("playing", "ready", "paused"):
        paddle_a.move_down()


def paddle_b_up():
    if state in ("playing", "ready", "paused"):
        paddle_b.move_up()


def paddle_b_down():
    if state in ("playing", "ready", "paused"):
        paddle_b.move_down()


wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")
wn.onkeypress(start_game, "space")
wn.onkeypress(toggle_pause, "p")
wn.onkeypress(restart_game, "r")


def update_game():
    global score_a, score_b

    ball.move()

    if ball.ycor > HEIGHT / 2 - 20:
        ball.sety(HEIGHT / 2 - 20)
        ball.dy *= -1
    elif ball.ycor < -(HEIGHT / 2 - 20):
        ball.sety(-(HEIGHT / 2 - 20))
        ball.dy *= -1

    if ball.xcor > WIDTH / 2 + 20:
        score_a += 1
        draw_score()
        if score_a >= WIN_SCORE:
            end_game("Player 1")
            return
        ball.serve(-1)

    elif ball.xcor < -(WIDTH / 2 + 20):
        score_b += 1
        draw_score()
        if score_b >= WIN_SCORE:
            end_game("Player 2")
            return
        ball.serve(1)

    if (ball.dx > 0) and (ball.xcor >= paddle_b.xcor - 20) and (ball.xcor <= paddle_b.xcor + 20) and (
        ball.ycor < paddle_b.ycor + PADDLE_HEIGHT / 2
    ) and (ball.ycor > paddle_b.ycor - PADDLE_HEIGHT / 2):
        ball.setx(paddle_b.xcor - 20)
        bounce_paddle(paddle_b, -1)

    if (ball.dx < 0) and (ball.xcor <= paddle_a.xcor + 20) and (ball.xcor >= paddle_a.xcor - 20) and (
        ball.ycor < paddle_a.ycor + PADDLE_HEIGHT / 2
    ) and (ball.ycor > paddle_a.ycor - PADDLE_HEIGHT / 2):
        ball.setx(paddle_a.xcor + 20)
        bounce_paddle(paddle_a, 1)


draw_score()
show_status("Press Space to start")
ball.serve(1)

while True:
    wn.update()

    if state == "playing":
        update_game()

    if state == "ready":
        ball.t.goto(0, 0)

    if state == "game_over":
        ball.t.goto(0, 0)

    if state == "paused":
        pass
