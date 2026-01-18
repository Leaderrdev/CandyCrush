import tkinter as tk
from tkinter import ttk
import random

# ================= CONSTANTE =================

COLOR_MAP = {
    0: '#f8f9fa',  # Culoare pentru celula goală (gri foarte deschis)
    1: '#ff6b6b',  # Bomboana roșie (gradient friendly)
    2: '#ffa94d',  # Bomboana portocalie
    3: '#51cf66',  # Bomboana verde
    4: '#74c0fc'  # Bomboana albastră
}

GRADIENT_LIGHT = {
    0: '#ffffff',
    1: '#ff8787',
    2: '#ffc078',
    3: '#69db7c',
    4: '#91d7ff'
}

CELL_SIZE = 50
PADDING = 8
SWAP_COLOR = '#9775fa'
MATCH_COLOR = '#ff6b6b'
BORDER_RADIUS = 12


# ================= LOGICA =================

class Formation:
    def __init__(self, cells):
        self.cells = set(cells)
        self.score = len(self.cells) * 10


class Board:
    def __init__(self, rows, cols, seed=None):
        self.rows = rows
        self.cols = cols
        self.rng = random.Random(seed)
        self.grid = [
            [self.rng.randint(1, 4) for _ in range(cols)]
            for _ in range(rows)
        ]

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def cell(self, r, c):
        return self.grid[r][c]

    def swap(self, a, b):
        (r1, c1), (r2, c2) = a, b
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]

    def detect_formations(self):
        forms = []

        # Detectare orizontală
        for r in range(self.rows):
            c = 0
            while c < self.cols - 2:
                v = self.grid[r][c]
                if v != 0 and self.grid[r][c + 1] == v and self.grid[r][c + 2] == v:
                    cells = [(r, c), (r, c + 1), (r, c + 2)]
                    c2 = c + 3
                    while c2 < self.cols and self.grid[r][c2] == v:
                        cells.append((r, c2))
                        c2 += 1
                    forms.append(Formation(cells))
                    c = c2
                else:
                    c += 1

        # Detectare verticală
        for c in range(self.cols):
            r = 0
            while r < self.rows - 2:
                v = self.grid[r][c]
                if v != 0 and self.grid[r + 1][c] == v and self.grid[r + 2][c] == v:
                    cells = [(r, c), (r + 1, c), (r + 2, c)]
                    r2 = r + 3
                    while r2 < self.rows and self.grid[r2][c] == v:
                        cells.append((r2, c))
                        r2 += 1
                    forms.append(Formation(cells))
                    r = r2
                else:
                    r += 1

        return forms

    def apply_eliminations(self, forms):
        for f in forms:
            for r, c in f.cells:
                self.grid[r][c] = 0

    def apply_gravity_and_refill(self):
        for c in range(self.cols):
            write = self.rows - 1
            for r in range(self.rows - 1, -1, -1):
                if self.grid[r][c] != 0:
                    self.grid[write][c] = self.grid[r][c]
                    write -= 1
            for r in range(write, -1, -1):
                self.grid[r][c] = self.rng.randint(1, 4)


# ================= UI =================

class CandyUI:
    def __init__(self, root):
        self.root = root
        self.board = Board(11, 11)
        self.score = 0
        self.swaps = 0
        self.running = False
        self.swap_cells = set()
        self.match_cells = set()
        self.speed = 1400

        # Configurare stil modern
        self.root.configure(bg='#1e1e2e')

        # Header cu gradient
        header = tk.Frame(root, bg='#2d2d44', height=80)
        header.pack(fill='x', pady=(0, 10))

        title = tk.Label(
            header,
            text="🍬 CANDY CRUSH",
            font=('Segoe UI', 24, 'bold'),
            fg='#ff6b6b',
            bg='#2d2d44'
        )
        title.pack(pady=15)

        # Panel de control modern
        ctrl = tk.Frame(root, bg='#1e1e2e')
        ctrl.pack(pady=10)

        # Stil pentru butoane
        btn_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'relief': 'flat',
            'bd': 0,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }

        play_btn = tk.Button(
            ctrl,
            text="▶ PLAY",
            command=self.start,
            bg='#51cf66',
            fg='white',
            activebackground='#69db7c',
            **btn_style
        )
        play_btn.pack(side='left', padx=5)

        stop_btn = tk.Button(
            ctrl,
            text="⏸ STOP",
            command=self.stop,
            bg='#ff6b6b',
            fg='white',
            activebackground='#ff8787',
            **btn_style
        )
        stop_btn.pack(side='left', padx=5)

        # Speed control cu stil modern
        speed_frame = tk.Frame(ctrl, bg='#2d2d44', relief='flat')
        speed_frame.pack(side='left', padx=15)

        tk.Label(
            speed_frame,
            text="⚡ Viteză (ms):",
            font=('Segoe UI', 10),
            fg='#a6adc8',
            bg='#2d2d44'
        ).pack(side='left', padx=5)

        self.speed_var = tk.IntVar(value=self.speed)
        speed_spin = tk.Spinbox(
            speed_frame,
            from_=300,
            to=3000,
            increment=200,
            textvariable=self.speed_var,
            width=6,
            font=('Segoe UI', 10),
            bg='#1e1e2e',
            fg='#cdd6f4',
            relief='flat',
            bd=2,
            buttonbackground='#313244',
            insertbackground='#cdd6f4'
        )
        speed_spin.pack(side='left', padx=5)

        # Status bar modern
        status_frame = tk.Frame(ctrl, bg='#2d2d44', relief='flat')
        status_frame.pack(side='left', padx=15)

        self.status = tk.Label(
            status_frame,
            text="",
            font=('Segoe UI', 11, 'bold'),
            fg='#ffa94d',
            bg='#2d2d44',
            padx=15,
            pady=5
        )
        self.status.pack()

        # Canvas cu margini rotunjite
        w = 11 * (CELL_SIZE + PADDING) + PADDING
        h = 11 * (CELL_SIZE + PADDING) + PADDING

        canvas_frame = tk.Frame(root, bg='#2d2d44', relief='flat', bd=0)
        canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=w,
            height=h,
            bg='#1e1e2e',
            highlightthickness=0,
            relief='flat'
        )
        self.canvas.pack(padx=10, pady=10)

        self.draw()
        self.update_status()

    def start(self):
        self.running = True
        self.loop()

    def stop(self):
        self.running = False
        self.swap_cells.clear()
        self.match_cells.clear()
        self.draw()

    def loop(self):
        if not self.running:
            return

        self.speed = max(200, int(self.speed_var.get()))
        move = self.find_any_swap()

        if move is None:
            self.running = False
            return

        a, b = move
        self.swap_cells = {a, b}
        self.draw()
        self.root.after(self.speed, lambda: self.apply_swap(a, b))

    def apply_swap(self, a, b):
        self.swap_cells.clear()
        self.board.swap(a, b)
        self.swaps += 1
        self.update_status()
        self.draw()
        self.root.after(self.speed, self.resolve_step)

    def resolve_step(self):
        forms = self.board.detect_formations()
        if not forms:
            self.root.after(self.speed, self.loop)
            return

        self.match_cells = set()
        for f in forms:
            self.match_cells |= f.cells

        self.draw()
        self.root.after(self.speed, lambda: self.apply_forms(forms))

    def apply_forms(self, forms):
        self.score += sum(f.score for f in forms)
        self.board.apply_eliminations(forms)
        self.board.apply_gravity_and_refill()
        self.match_cells.clear()
        self.update_status()
        self.draw()
        self.root.after(self.speed, self.resolve_step)

    def find_any_swap(self):
        for r in range(11):
            for c in range(11):
                for dr, dc in ((1, 0), (0, 1)):
                    r2, c2 = r + dr, c + dc
                    if not self.board.in_bounds(r2, c2):
                        continue
                    copy = Board(11, 11)
                    copy.grid = [row[:] for row in self.board.grid]
                    copy.swap((r, c), (r2, c2))
                    if copy.detect_formations():
                        return (r, c), (r2, c2)
        return None

    def draw(self):
        self.canvas.delete("all")

        for r in range(11):
            for c in range(11):
                v = self.board.cell(r, c)
                x1 = PADDING + c * (CELL_SIZE + PADDING)
                y1 = PADDING + r * (CELL_SIZE + PADDING)
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                # Umbre pentru efect 3D
                shadow_offset = 3
                self.canvas.create_oval(
                    x1 + shadow_offset, y1 + shadow_offset,
                    x2 + shadow_offset, y2 + shadow_offset,
                    fill='#11111b', outline=''
                )

                # Gradient effect prin suprapunere de cercuri
                if (r, c) in self.swap_cells:
                    outline_color = SWAP_COLOR
                    width = 4
                elif (r, c) in self.match_cells:
                    outline_color = MATCH_COLOR
                    width = 4
                    # Pulsare pentru match
                    self.canvas.create_oval(
                        x1 - 3, y1 - 3, x2 + 3, y2 + 3,
                        outline=MATCH_COLOR,
                        width=2,
                        dash=(4, 4)
                    )
                else:
                    outline_color = '#313244'
                    width = 2

                # Bomboana principală
                self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=COLOR_MAP[v],
                    outline=outline_color,
                    width=width
                )

                # Highlight pentru efect lucios
                if v != 0:
                    highlight_size = CELL_SIZE // 4
                    self.canvas.create_oval(
                        x1 + CELL_SIZE // 4,
                        y1 + CELL_SIZE // 5,
                        x1 + CELL_SIZE // 4 + highlight_size,
                        y1 + CELL_SIZE // 5 + highlight_size,
                        fill=GRADIENT_LIGHT[v],
                        outline=''
                    )

    def update_status(self):
        self.status.config(text=f"🏆 Scor: {self.score}  |  🔄 Mutări: {self.swaps}")


# ================= MAIN =================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Candy Crush - Modern Edition")
    root.resizable(False, False)
    CandyUI(root)
    root.mainloop()