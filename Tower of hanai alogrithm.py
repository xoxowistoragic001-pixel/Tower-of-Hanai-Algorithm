
import tkinter as tk
from tkinter import messagebox

WIDTH = 800
HEIGHT = 500
ROD_Y = 400          # Rods ka neeche ka hissa
ROD_HEIGHT = 300     # Rod ki height
DISK_HEIGHT = 25     # Har disk ki height
BASE_Y = 440         # Base line


ROD_X = [150, 400, 650]

COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
          "#1abc9c", "#e67e22", "#34495e"]


class HanoiGame:
    def __init__(self, root, n):
        self.root = root
        self.n = n
        self.rods = [list(range(n, 0, -1)), [], []]
        self.moves = 0
        self.selected_rod = None
        self.disk_items = {}   
        self.animating = False

        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#f0f0f0")
        self.canvas.pack()

      
        self.canvas.create_text(WIDTH // 2, 30,
                                text=f"Tower of Hanoi  —  {n} Disks",
                                font=("Arial", 20, "bold"), fill="#2c3e50")

        self.info = self.canvas.create_text(WIDTH // 2, 65,
                                            text="Moves: 0   |   Minimum: " + str(2**n - 1),
                                            font=("Arial", 13), fill="#555")

        
        self.canvas.create_rectangle(50, BASE_Y, WIDTH - 50, BASE_Y + 15,
                                     fill="#8b4513", outline="")

        
        for x in ROD_X:
            self.canvas.create_rectangle(x - 5, ROD_Y - ROD_HEIGHT,
                                         x + 5, ROD_Y,
                                         fill="#8b4513", outline="")

        
        for i, x in enumerate(ROD_X):
            self.canvas.create_text(x, BASE_Y + 40,
                                    text=f"Rod {i+1}",
                                    font=("Arial", 14, "bold"))

        
        self.draw_all_disks()

        
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="🔄 Reset", font=("Arial", 12),
                  command=self.reset).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🤖 Auto Solve", font=("Arial", 12),
                  command=self.auto_solve).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Quit", font=("Arial", 12),
                  command=root.destroy).pack(side=tk.LEFT, padx=5)

        
        self.canvas.bind("<Button-1>", self.on_click)

        
        self.canvas.create_text(WIDTH // 2, HEIGHT - 15,
                                text="Click on rd: Source,  destination",
                                font=("Arial", 10, "italic"), fill="#777")

  
    def disk_width(self, size):
        return 40 + size * 30

    def disk_color(self, size):
        return COLORS[(size - 1) % len(COLORS)]

    def disk_position(self, rod_index, slot):
        x = ROD_X[rod_index]
        y = ROD_Y - DISK_HEIGHT // 2 - slot * DISK_HEIGHT
        return x, y

    def draw_disk(self, size, rod_index, slot):
        x, y = self.disk_position(rod_index, slot)
        w = self.disk_width(size)
        item = self.canvas.create_rectangle(
            x - w // 2, y - DISK_HEIGHT // 2,
            x + w // 2, y + DISK_HEIGHT // 2,
            fill=self.disk_color(size), outline="#333", width=2
        )
        text = self.canvas.create_text(x, y, text=str(size),
                                       font=("Arial", 12, "bold"), fill="white")
        self.disk_items[size] = (item, text)

    def draw_all_disks(self):
        for item in self.disk_items.values():
            self.canvas.delete(item[0])
            self.canvas.delete(item[1])
        self.disk_items.clear()

        for rod_index, rod in enumerate(self.rods):
            for slot, size in enumerate(rod):
                self.draw_disk(size, rod_index, slot)


    def is_valid(self, src, dst):
        if not self.rods[src]:
            return False
        if not self.rods[dst]:
            return True
        return self.rods[src][-1] < self.rods[dst][-1]

    
    def move_disk_animated(self, src, dst, callback=None):
        if self.animating:
            return
        self.animating = True

        size = self.rods[src][-1]
        item, text = self.disk_items[size]

        # Utha do (upar le jao)
        start_x, start_y = self.disk_position(src, len(self.rods[src]) - 1)
        lift_y = 80

        # Step 1: upar
        self.animate(item, text, start_x, start_y, start_x, lift_y, 8, lambda: (
            # Step 2: horizontally
            self.animate(item, text, start_x, lift_y, ROD_X[dst], lift_y, 8, lambda: (
                # Step 3: neeche
                self.animate(item, text, ROD_X[dst], lift_y,
                             ROD_X[dst], self.disk_position(dst, len(self.rods[dst]))[1],
                             8, lambda: self.finish_move(src, dst, size, callback))
            ))
        ))

    def animate(self, item, text, x1, y1, x2, y2, steps, done):
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps
        count = [0]

        def step():
            if count[0] < steps:
                self.canvas.move(item, dx, dy)
                self.canvas.move(text, dx, dy)
                count[0] += 1
                self.root.after(15, step)
            else:
                done()

        step()

    def finish_move(self, src, dst, size, callback):
        # Data update
        self.rods[src].pop()
        self.rods[dst].append(size)
        self.moves += 1
        self.canvas.itemconfig(self.info,
                               text=f"Moves: {self.moves}   |   Minimum: {2**self.n - 1}")
        self.animating = False

        # Check win
        if len(self.rods[2]) == self.n:
            self.root.after(300, lambda: messagebox.showinfo(
                " You Win!",
                f"Congratulations!\nMoves: {self.moves}\nMinimum: {2**self.n - 1}"
            ))

        if callback:
            self.root.after(200, callback)

 
    def on_click(self, event):
        if self.animating:
            return

        # Kaunsi rod par click hua?
        clicked = None
        for i, x in enumerate(ROD_X):
            if abs(event.x - x) < 80:
                clicked = i
                break

        if clicked is None:
            return

        if self.selected_rod is None:
            # Pehli click — source choose
            if self.rods[clicked]:
                self.selected_rod = clicked
                self.highlight_rod(clicked)
        else:
            src = self.selected_rod
            dst = clicked
            self.unhighlight_rod(src)
            self.selected_rod = None

            if src == dst:
                return

            if self.is_valid(src, dst):
                self.move_disk_animated(src, dst)
            else:
                self.flash_error(dst)

    def highlight_rod(self, i):
        x = ROD_X[i]
        self.canvas.create_rectangle(x - 60, ROD_Y - ROD_HEIGHT - 10,
                                     x + 60, ROD_Y + 10,
                                     outline="#f1c40f", width=4, tags="highlight")

    def unhighlight_rod(self, i):
        self.canvas.delete("highlight")

    def flash_error(self, rod):
        x = ROD_X[rod]
        rect = self.canvas.create_rectangle(x - 60, ROD_Y - ROD_HEIGHT - 10,
                                            x + 60, ROD_Y + 10,
                                            outline="red", width=4)
        self.root.after(300, lambda: self.canvas.delete(rect))

    
    def auto_solve(self):
        if self.animating:
            return
        self.reset()
        self.root.after(300, lambda: self._solve(self.n, 0, 1, 2))

    def _solve(self, n, src, helper, dst):
        if n == 0:
            return
        self._solve(n - 1, src, dst, helper)
        self.move_disk_animated(src, dst,
                                callback=lambda: self._solve(n - 1, helper, src, dst))
       

    
    def reset(self):
        self.animating = False
        self.rods = [list(range(self.n, 0, -1)), [], []]
        self.moves = 0
        self.selected_rod = None
        self.canvas.delete("highlight")
        self.draw_all_disks()
        self.canvas.itemconfig(self.info,
                               text=f"Moves: 0   |   Minimum: {2**self.n - 1}")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tower of Hanoi")

    # Disks poochho
    from tkinter import simpledialog
    n = simpledialog.askinteger("Disks", "Disks? (1-7)", minvalue=1, maxvalue=7)
    if n is None:
        n = 3

    HanoiGame(root, n)
    root.mainloop()
