import tkinter as tk
from psutil import cpu_percent
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from random import randint
import matplotlib.dates as mdates
import AntiDOSWeb
import seaborn as sns

class GraphPage(tk.Frame):

    def __init__(self, parent, num_segs, anti_dos):

        sns.set_style("whitegrid")
        blue, = sns.color_palette("muted", 1)

        # nb_points: number of points for the graph
        tk.Frame.__init__(self, parent)
        # matplotlib figure
        self.figure = Figure(figsize=(14, 7), dpi=100)
        self.figure.set_facecolor('#2CB57E')  
        self.figure.suptitle("Peticiones recibidas por segundo", fontsize=16)
        self.ax = self.figure.add_subplot(111)

        # format the x-axis to show the time
        myFmt = mdates.DateFormatter("%H:%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        # initial x and y data
        dateTimeObj = datetime.now() + timedelta(seconds=-num_segs)
        self.x_data = [dateTimeObj + timedelta(seconds=i) for i in range(num_segs)]
        self.y_data = [0 for i in range(num_segs)]

        # create the plot
        self.plot = self.ax.plot(self.x_data, self.y_data, color=blue, label='Peticiones')[0]
        self.ax.fill_between(self.x_data, 0, self.y_data, alpha=.3)

        self.ax.set_ylim(0, 10)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])

        self.ax.grid('on')
        self.ax.set_facecolor('#C5DECD')  
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.anti_dos = anti_dos



    def nuevoElemento(self, tiempo):
        horas_actividad = self.anti_dos.extraerHorasActividad()
        elemento = 0
        if tiempo-1 in horas_actividad:
            elemento = horas_actividad[tiempo-1]

        return elemento

    def animate(self):
        # append new data point to the x and y data
        ahora = datetime.now()
        self.x_data.append(ahora)
        self.y_data.append(self.nuevoElemento(int(ahora.timestamp())))
        # remove oldest data point
        self.x_data = self.x_data[1:]
        self.y_data = self.y_data[1:]
        #  update plot data
        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])
        self.ax.set_ylim(0, 10 if (max(self.y_data) < 10) else int(max(self.y_data)*1.1))
        self.canvas.draw_idle()  # redraw plot
        self.after(1000, self.animate)  # repeat after 1s