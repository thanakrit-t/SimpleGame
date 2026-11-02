""" Develop by Thanakrit
"""
import tkinter as tk
import random


CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
GAME_SPEED = 100


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.score = 0
        self.high_score = 0
        self.running = False
        self.paused = False
        self.snake = []
        self.food = None
        self.direction = "Right"
        self.next_direction = "Right"
        self.job = None

        self.score_label = tk.Label(
            root, text="Score: 0    High Score: 0",
            font=("Arial", 14, "bold"), anchor="w"
        )
        self.score_label.pack(fill="x", padx=10, pady=(8, 4))

        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#16213e",
            highlightthickness=2,
            highlightbackground="#0f3460"
        )
        self.canvas.pack(padx=10, pady=(0, 10))

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("w", lambda event: self.change_direction("Up"))
        self.root.bind("s", lambda event: self.change_direction("Down"))
        self.root.bind("a", lambda event: self.change_direction("Left"))
        self.root.bind("d", lambda event: self.change_direction("Right"))
        self.root.bind("<space>", lambda event: self.toggle_pause())
        self.root.bind("<Return>", lambda event: self.start_game())

        self.draw_start_screen()

    def draw_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE / 2,
            GRID_HEIGHT * CELL_SIZE / 2 - 30,
            text="SNAKE",
            fill="#e94560",
            font=("Arial", 32, "bold")
        )
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE / 2,
            GRID_HEIGHT * CELL_SIZE / 2 + 20,
            text="Press Enter or click Start",
            fill="white",
            font=("Arial", 14)
        )

        self.start_button = tk.Button(
            self.root, text="Start Game", font=("Arial", 12, "bold"),
            bg="#e94560", fg="white", activebackground="#c73651",
            command=self.start_game
        )
        self.start_button.pack(pady=(0, 10))

    def start_game(self, event=None):
        if getattr(self, "start_button", None) is not None:
            self.start_button.destroy()
            self.start_button = None

        if self.job is not None:
            self.root.after_cancel(self.job)

        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.running = True
        self.paused = False
        self.update_score()
        self.spawn_food()
        self.draw_game()
        self.job = self.root.after(GAME_SPEED, self.tick)

    def spawn_food(self):
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
        ]
        self.food = random.choice(empty_cells) if empty_cells else None

    def change_direction(self, new_direction):
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if self.running and new_direction != opposite.get(self.direction):
            self.next_direction = new_direction

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.draw_pause_overlay()
        else:
            self.canvas.delete("pause_overlay")
            self.job = self.root.after(GAME_SPEED, self.tick)

    def draw_pause_overlay(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.canvas.create_rectangle(
            0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE,
            fill="#000000", stipple="gray50", tags="pause_overlay"
        )
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE / 2,
            GRID_HEIGHT * CELL_SIZE / 2,
            text="PAUSED",
            fill="white",
            font=("Arial", 24, "bold"),
            tags="pause_overlay"
        )

    def tick(self):
        if not self.running or self.paused:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)
        hit_wall = not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT)
        moving_into_tail = new_head == self.snake[-1] and new_head != self.food
        hit_self = new_head in self.snake and not moving_into_tail

        if hit_wall or hit_self:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.update_score()
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw_game()
        self.job = self.root.after(GAME_SPEED, self.tick)

    def draw_game(self):
        self.canvas.delete("all")

        if self.food is not None:
            x, y = self.food
            self.canvas.create_oval(
                x * CELL_SIZE + 3, y * CELL_SIZE + 3,
                (x + 1) * CELL_SIZE - 3, (y + 1) * CELL_SIZE - 3,
                fill="#e94560", outline="#ff6b81"
            )

        for index, (x, y) in enumerate(self.snake):
            color = "#53d769" if index == 0 else "#3fa34d"
            self.canvas.create_rectangle(
                x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE - 1,
                fill=color, outline="#16213e"
            )

        if self.food is None:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE / 2,
                GRID_HEIGHT * CELL_SIZE / 2,
                text="You Win!",
                fill="white",
                font=("Arial", 24, "bold")
            )

    def update_score(self):
        self.high_score = max(self.high_score, self.score)
        self.score_label.config(
            text=f"Score: {self.score}    High Score: {self.high_score}"
        )

    def game_over(self):
        self.running = False
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.canvas.create_rectangle(
            0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE,
            fill="#000000", stipple="gray50"
        )
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE / 2,
            GRID_HEIGHT * CELL_SIZE / 2 - 20,
            text="GAME OVER",
            fill="#e94560",
            font=("Arial", 26, "bold")
        )
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE / 2,
            GRID_HEIGHT * CELL_SIZE / 2 + 25,
            text=f"Score: {self.score} — Press Enter to restart",
            fill="white",
            font=("Arial", 14)
        )


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
