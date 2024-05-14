import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import seaborn as sns


class GraphPage(tk.Frame):
    """Clase que representa una página de gráficos en una aplicación Tkinter.

    Esta clase genera un gráfico de líneas en tiempo real utilizando
    matplotlib y tkinter.

    Attributes:
        num_segs (int): Número de segmentos de tiempo a mostrar en el gráfico.
        max_segs (int): Número máximo de segmentos de tiempo a considerar en el histórico.
        anti_dos (AntiDos): Objeto AntiDos utilizado para extraer datos de actividad.
        graph_color (str): Color utilizado para dibujar el gráfico.
        figure (Figure): Objeto Figure de matplotlib para el gráfico.
        ax (Axes): Eje del gráfico.
        canvas (FigureCanvasTkAgg): Canvas de tkinter para el gráfico.
    """

    def __init__(self, parent, num_segs, anti_dos, max_segs, color=""):
        """Inicializa una nueva instancia de la clase GraphPage.

        Args:
            parent (tk.Tk): Ventana principal de la aplicación.
            num_segs (int): Número de segmentos de tiempo a mostrar en el gráfico.
            anti_dos (AntiDos): Objeto AntiDos utilizado para extraer datos de actividad.
            max_segs (int): Número máximo de segmentos de tiempo a considerar en el histórico.
            color (str, optional): Color del gráfico. Defaults to "".
        """
        self.num_segs = num_segs
        self.max_segs = max_segs
        sns.set_style("whitegrid")

        if not color:
            self.graph_color, = sns.color_palette("muted", 1).as_hex()
        else:
            self.graph_color = color

        # Inicialización del frame de tkinter
        tk.Frame.__init__(self, parent)

        # Inicialización de la figura de matplotlib
        self.figure = Figure(figsize=((parent.winfo_screenwidth() / 137), (parent.winfo_screenheight() / 190)), dpi=100)
        self.figure.set_facecolor('#2CB57E')
        self.figure.suptitle("Peticiones recibidas por segundo", fontsize=16)
        self.ax = self.figure.add_subplot(111)

        # Formato del eje x para mostrar la hora
        myFmt = mdates.DateFormatter("%H:%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        self.anti_dos = anti_dos

        # Datos iniciales para el eje x e y
        dateTimeObj = datetime.now() + timedelta(seconds=-max_segs)
        self.full_x_data = [
            dateTimeObj + timedelta(seconds=i) for i in range(max_segs)
        ]
        self.full_y_data = self.extraerNumPeticiones(self.full_x_data)

        self.setTime(num_segs)

        # Creación del gráfico
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

        # Creación del canvas de tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                         fill=tk.BOTH,
                                         expand=True)
        self.animate()

    def extraerNumPeticiones(self, x_valores):
        """Extrae el número de peticiones para cada valor de tiempo en x_valores.

        Args:
            x_valores (list): Lista de valores de tiempo.

        Returns:
            list: Lista de números de peticiones correspondientes a cada valor de tiempo.
        """
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
        """Cambia el color del gráfico.

        Args:
            color (str): Nuevo color para el gráfico.
        """
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
        """Calcula el número de peticiones para un valor de tiempo dado.

        Args:
            tiempo (int): Valor de tiempo.

        Returns:
            int: Número de peticiones para el valor de tiempo dado.
        """
        horas_actividad = self.anti_dos.extraerHorasActividad(tiempo)
        elemento = 0
        tiempo = int(tiempo)
        if tiempo - 1 in horas_actividad:
            elemento = horas_actividad[tiempo - 1]

        return elemento

    def setTime(self, tiempo):
        """Actualiza el rango de tiempo mostrado en el gráfico.

        Args:
            tiempo (int): Número de segmentos de tiempo a mostrar.
        """
        self.x_data = self.full_x_data[self.max_segs - tiempo:]
        self.y_data = self.full_y_data[self.max_segs - tiempo:]

        self.num_segs = tiempo

    def animate(self):
        """Actualiza el gráfico con nuevos datos en tiempo real."""
        ahora = datetime.now()
        self.full_x_data.append(ahora)
        self.full_y_data.append(self.nuevoElemento(int(ahora.timestamp())))
        self.full_x_data = self.full_x_data[1:]
        self.full_y_data = self.full_y_data[1:]
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
        self.canvas.draw_idle()
