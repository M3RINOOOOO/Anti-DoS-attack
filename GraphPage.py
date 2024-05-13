import tkinter as tk
from psutil import cpu_percent
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from random import randint
import matplotlib.dates as mdates
import seaborn as sns


class GraphPage(tk.Frame):

    def __init__(self, parent, num_segs, anti_dos, max_segs, color=""):
        self.num_segs = num_segs
        self.max_segs = max_segs
        sns.set_style("whitegrid")
        self.graph_color, = sns.color_palette("muted", 1) if not color else color
        #self.graph_color = "red"

        # nb_points: number of points for the graph
        tk.Frame.__init__(self, parent)
        # matplotlib figure
        self.figure = Figure(figsize=(14, 6), dpi=100)
        self.figure.set_facecolor('#2CB57E')
        self.figure.suptitle("Peticiones recibidas por segundo", fontsize=16)
        self.ax = self.figure.add_subplot(111)

        # format the x-axis to show the time
        myFmt = mdates.DateFormatter("%H:%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        self.anti_dos = anti_dos

        # initial x and y data
        dateTimeObj = datetime.now() + timedelta(seconds=-max_segs)
        self.full_x_data = [
            dateTimeObj + timedelta(seconds=i) for i in range(max_segs)
        ]
        self.full_y_data = self.extraerNumPeticiones(self.full_x_data)

        self.setTime(num_segs)

        # create the plot
        self.plot = self.ax.plot(self.x_data,
                                 self.y_data,
                                 color=self.graph_color,
                                 label='Peticiones')[0]
        self.fill_between = self.ax.fill_between(self.x_data,
                                                 0,
                                                 self.y_data,
                                                 alpha=.3,
                                                 color=self.graph_color)

        self.ax.set_ylim(0, 10)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])

        self.ax.grid('on')
        self.ax.set_facecolor('#C5DECD')

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                         fill=tk.BOTH,
                                         expand=True)
        self.animate()

    #[self.nuevoElemento(int(self.full_x_data[i].timestamp())) for i in range(max_segs)]
    def extraerNumPeticiones(self, x_valores):
        horas_actividad = self.anti_dos.extraerHorasActividad()
        y_valores = []
        peticiones = 0
        for t in x_valores:
            peticiones = 0
            tiempo = int(t.timestamp())
            if tiempo - 1 in horas_actividad:
                peticiones = horas_actividad[tiempo - 1]

            y_valores.append(peticiones)

        return y_valores

    def cambiarColor(self, color):
        self.graph_color = color
        self.plot = self.ax.plot(self.x_data,
                                 self.y_data,
                                 color=color,
                                 label='Peticiones')[0]
        self.fill_between.remove()
        self.fill_between = self.ax.fill_between(self.x_data,
                                                 0,
                                                 self.y_data,
                                                 alpha=.3,
                                                 color=color)

    def nuevoElemento(self, tiempo):
        horas_actividad = self.anti_dos.extraerHorasActividad(tiempo)
        elemento = 0
        tiempo = int(tiempo)
        if tiempo - 1 in horas_actividad:
            elemento = horas_actividad[tiempo - 1]

        return elemento

    def setTime(self, tiempo):
        self.x_data = self.full_x_data[self.max_segs - tiempo:]
        self.y_data = self.full_y_data[self.max_segs - tiempo:]

        self.num_segs = tiempo

    def animate(self):
        # append new data point to the x and y data
        ahora = datetime.now()
        self.full_x_data.append(ahora)
        self.full_y_data.append(self.nuevoElemento(int(ahora.timestamp())))
        # remove oldest data point
        self.full_x_data = self.full_x_data[1:]
        self.full_y_data = self.full_y_data[1:]
        #  update plot data
        self.setTime(self.num_segs)

        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.fill_between.remove()
        self.fill_between = self.ax.fill_between(self.x_data,
                                                 0,
                                                 self.y_data,
                                                 alpha=.3,
                                                 color=self.graph_color)

        self.ax.set_xlim(self.x_data[0], self.x_data[-1])
        self.ax.set_ylim(
            0, 10 if (max(self.y_data) < 10) else int(max(self.y_data) * 1.1))
        self.canvas.draw_idle()  # redraw plot
