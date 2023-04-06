from tkinter import *
import time
import random

tk = Tk()
tk.title("Python Game")
tk.resizable()
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
canvas.pack()
tk.update()

# Описываем класс Ball, который будет отвечать за шарик
class Ball:
    # конструктор — он вызывается в момент создания нового объекта на основе этого класса
    def __init__(self, canvas, paddle, score, color):
        # задаем параметры объекта, которые нам передают в скобках в момент создания шарика
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        # Цвет нужен был для того, чтоб закрасить весь шарик
        # Здесь появляется новое свойство id, в котором хранится внутреннее название шарика
        # Командой create oval создаем круг радиусом 15 пикселей, который закрашиваем нужным цветом
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        # Помещаем шарик в точку с координатами 245, 100
        self.canvas.move(self.id, 245, 100)
        # Список возможных координат для старта
        starts = [-2, -1, 1, 2]
        # Перемешиваем координаты
        random.shuffle(starts)
        # Выбираем первый из перемешенного, он будет вектором движения шарика
        self.x = starts[0]
        # Сначала он всегда падает вниз, по этому необходимо уменьшить значение по оси Y
        self.y = -2
        # Шарик узнает свою высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # Узнаем, достиг ли шарик дна. Пока не достиг, значение будет False
        self.hit_bottom = False

    # Обрабатываем касание платформы. Для этого получаем 4 координаты шарика в переменной pos (левая верхняя и прававя нижняя точки)
    def hit_paddle(self, pos):
        # Получаем координаты платформы через объект paddle (платформа)
        paddle_pos = self.canvas.cords(self.paddle.id)
        # Если координаты касания совпадают с координатами платформы
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                # Увеличиваем счет
                self.score.hit()
                # Возвращваем метку о том, что успешно коснулись
                return True
            # Либо False - касания не было
            return False

    def draw(self):
        # сдвигаем нашу платформу на заданное количество пикселей
        self.canvas.move(self.id, self.x, 0)
        # получаем координаты холста
        pos = self.canvas.coords(self.id)
        # если мы упёрлись в левую границу
        if pos[0] <= 0:
            # останавливаемся
            self.y = 0
        # если упёрлись в правую границу
        elif pos[2] >= self.canvas_width:
            # останавливаемся
            self.y = 0

# Описываем класс платформы
class Paddle:
    # конструктор
    def __init__(self, canvas, color):
        # canvas означает, что платформа будет нарисована на нашем изначальном холсте
        self.canvas = canvas
        # создаём прямоугольную платформу 10 на 100 пикселей, закрашиваем выбранным цветом и получаем её внутреннее имя
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        # задаём список возможных стартовых положений платформы
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        # перемешиваем их
        random.shuffle(start_1)
        # выбираем первое из перемешанных
        self.starting_point_x = start_1[0]
        # перемещаем платформу в стартовое положение
        self.canvas.move(self.id, self.starting_point_x, 300)
        # пока платформа никуда не движется, поэтому изменений по оси х нет
        self.x = 0
        # платформа узнаёт свою ширину
        self.canvas_width = self.canvas.winfo_width()
        # задаём обработчик нажатий
        # если нажата стрелка вправо — выполняется метод turn_right()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        # если стрелка влево — turn_left()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        # пока платформа не двигается, поэтому ждём
        self.started = False
        # как только игрок нажмёт Enter — всё стартует
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)
    # движемся вправо
    def turn_right(self, event):
        # будем смещаться правее на 2 пикселя по оси х
        self.x = 2
    # движемся влево
    def turn_left(self, event):
        # будем смещаться левее на 2 пикселя по оси х
        self.x = -2
    # игра начинается
    def start_game(self, event):
        # меняем значение переменной, которая отвечает за старт движения платформы
        self.started = True
    # метод, который отвечает за движение платформы
    def draw(self):
        # сдвигаем нашу платформу на заданное количество пикселей
        self.canvas.move(self.id, self.x, 0)
        # получаем координаты холста
        pos = self.canvas.coords(self.id)
        # если мы упёрлись в левую границу
        if pos[0] <= 0:
            # останавливаемся
            self.x = 0
        # если упёрлись в правую границу
        elif pos[2] >= self.canvas_width:
            # останавливаемся
            self.x = 0

class Score: # Описываем класс score
    def __init__(self, canvas, color): # Конструктор
        self.score = 0 # Вначале счет равен нулю
        self.canvas = canvas # используем холст от шарика
        self.id = canvas.create_text(450, 10, text=self.score, font =('Courier', 15), fill=color)
        # Обрабатываем касание платформы
        def hit(self):
            self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)

# создаём объект — зелёный счёт
score = Score(canvas, 'green')
# создаём объект — белую платформу
paddle = Paddle(canvas, 'White')
# создаём объект — красный шарик
ball = Ball(canvas, paddle, score, 'red')
# пока шарик не коснулся дна
while not ball.hit_bottom:
    # если игра началась и платформа может двигаться
    if paddle.started == True:
        # двигаем шарик
        ball.draw()
        # двигаем платформу
        paddle.draw()
    # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
    tk.update_idletasks()
    # обновляем игровое поле, и смотрим за тем, чтобы всё, что должно было быть сделано — было сделано
    tk.update()
    # замираем на одну сотую секунды, чтобы движение элементов выглядело плавно
    time.sleep(0.01)
# если программа дошла досюда, значит, шарик коснулся дна. Ждём 3 секунды, пока игрок прочитает финальную надпись, и завершаем игру
time.sleep(3)