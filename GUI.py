from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

root = Tk()
root.title('Home Page')
root.geometry('1280x720')


def onClickURL():
    w1 = Tk()
    w1.title('Edit URLs')
    w1.geometry('620x480')

    def onClickAdd():
        pass

    def onClickDel():
        pass



    bt1 = Button(w1, text="Add URLs", command=onClickAdd)
    bt1.pack()

    bt2 = Button(w1, text='Delete URLs', command=onClickDel)
    bt2.pack()

    w1.mainloop()


def onClickVary():
    w2 = Tk()
    w2.title('Price Variations')
    w2.geometry('620x480') 
    w2.mainloop()


bt1 = Button(root, text="Edit URLs", command=onClickURL)
bt1.pack()

bt2 = Button(root, text='View Price Variations', command=onClickVary)
bt2.pack()

fig = Figure(figsize=(5, 5), dpi=100)

y = [i**2 for i in range(101)]

plot1 = fig.add_subplot(111)

plot1.plot(y)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()


canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

canvas.get_tk_widget().pack()

root.mainloop()