from tkinter import *
import random
from tkinter import messagebox


class minesweeper:
    def __init__(self):
        self.root = Tk()
        self.root.title("minesweeper")

        self.minesBoard = Frame(self.root)
        self.minesBoard.pack()

        self.board = game_board(30, 16, 99, self.minesBoard)
        self.board.create_mines()

    def game_over(self):
        pass


class game_board:
    def __init__(self, grid_size_x, grid_size_y, num_mines, place):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.num_mines = num_mines
        self.place = place
        global total_buttons
        total_buttons = grid_size_x * grid_size_y

    def create_mines(self):
        # 지뢰판 만들기
        self.mines = [[0 for i in range(self.grid_size_x)] for j in range(self.grid_size_y)]
        minesAddress = random.sample(range(self.grid_size_x*self.grid_size_y), self.num_mines)
        for i in minesAddress:
            self.mines[i//self.grid_size_x][i%self.grid_size_x] = 1

        global buttons
        buttons = [[None for i in range(self.grid_size_x)] for j in range(self.grid_size_y)]

        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                buttons[i][j] = mines_button(self.grid_size_x, self.grid_size_y, self.num_mines, self.place, self.mines, self.mines[i][j], i, j)

    def game_end(self, is_win):
        for i in self.place.grid_slaves():
            i.destroy()

        if is_win:
            label = Label(self.place, text="You're winner!!!")
            label.pack()
        else:
            label = Label(self.place, text="You're looser!!!")
            label.pack()



class mines_button(game_board):
    def __init__(self, grid_size_x, grid_size_y, num_mines, place, mines, is_mine, i, j):
        super().__init__(grid_size_x, grid_size_y, num_mines, place)
        self.mines = mines
        self.is_mine = is_mine
        self.i = i
        self.j = j
        self.nothing = PhotoImage(file="nothing.png")
        self.nothing = self.nothing.subsample(30, 30)
        self.flag = PhotoImage(file="flag.png")
        self.flag = self.flag.subsample(30, 30)
        self.is_right = False
        self.button = Button(self.place, image=self.nothing, command=self.click)
        self.button.bind("<Button-3>", self.change)
        self.button.grid(row=i, column=j)

    def click(self):
        # 버튼을 클릭했을 때
        global total_buttons
        self.button['state'] = DISABLED
        self.button['relief'] = GROOVE
        total_buttons -= 1

        if self.is_mine:
            self.game_end(False)
        else:
            cnt = self.count_mines(self.i, self.j)
            self.button.configure(width=2, height=1, image='', text=str(cnt))
            if cnt == 0:
                self.arroundZero(self.i, self.j)

            if total_buttons == self.num_mines:
                self.game_end(True)

    def count_mines(self, i, j):
        # 주변 지뢰 개수를 세는 함수
        count = 0
        for x in [-1, 0, 1]:
            if 0 <= x+j < self.grid_size_x:
                for y in [-1, 0, 1]:
                    if 0 <= y+i < self.grid_size_y:
                        if self.mines[y + i][x + j] == 1:
                            count += 1
        return count

    def arroundZero(self, i, j):
        # 주변 지뢰 개수가 0일 때, 주변 버튼 모두 클릭
        for x in [-1, 0, 1]:
            if 0 <= x+j < self.grid_size_x:
                for y in [-1, 0, 1]:
                    if 0 <= y+i < self.grid_size_y:
                        buttons[y + i][x + j].button.invoke()

    def change(self, event):
        if not self.is_right:
            self.button['state'] = DISABLED
            self.button.configure(image=self.flag)
            self.is_right = True
        else:
            self.button['state'] = NORMAL
            self.button.configure(image=self.nothing)
            self.is_right = False



if __name__ == "__main__":
    game = minesweeper()
    game.root.mainloop()
