import numpy as np
from matplotlib import pyplot as plt
import csv
import pandas as pd
from scipy.optimize import curve_fit
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

#Se definen los rangos para el problema 1
xmargin = np.linspace(5, 15, 11)
ymargin = np.linspace(5, 25, 21)

#Estos vectores definen los márgenes del para cálculos como los momentos y la función de densidad
xxmargin = np.linspace(0, 15, 100)
yymargin = np.linspace(0, 25, 100)

#Se definen los vectores que guardan las probabilidades de X y Y
fx = []
fy = []

#Primero se plotean los datos, con esto se define la curva que mejor se adapta
def gaussiana(x, mu, sigma):
    return 1/np.sqrt(2*np.pi*sigma**2)*np.exp(-(x-mu)**2/(2*sigma**2))

#Esta función resuelve los puntos 1, 3, 4 
def margin_dens(datos1, datos2, fx, xmargin, xxmargin, fy, ymargin, yymargin):

    #se rellena el vector con las probabilidades de X y Y
    fx = np.sum(datos1, axis=1)
    fy = np.sum(datos1, axis=0)

    #se hace el ajuste de la distribución gaussiana a los datos "marginales" y se guardan los parámetros que las definen
    paramX,_=curve_fit(gaussiana, xmargin, fx)
    paramY,_=curve_fit(gaussiana, ymargin, fy)


    print("Los parámetros la distribución de X son: mu=" + str(paramX[0]) + " y sigma=" + str(paramX[1]) + "\n")
    print("Los parámetros la distribución de Y son: mu=" + str(paramY[0]) + " y sigma=" + str(paramY[1]) + "\n")

    #Se grafica la distribución con los datos ruidosos y el fit para la función de X
    plt.title("Ajuste para la función marginal valores de X")
    plt.plot(xmargin, fx)
    plt.plot(xmargin, gaussiana(xmargin, paramX[0], paramX[1]))
    #plt.show()
    plt.savefig("ajuste_fx.png")
    plt.close()

    #Se grafica la distribución con los datos ruidosos y el fit para la función de Y
    plt.title("Ajuste para la función marginal valores de Y")
    plt.plot(ymargin, fy)
    plt.plot(ymargin, gaussiana(ymargin, paramY[0], paramY[1]))
    #plt.show()
    plt.savefig("ajuste_fy.png")
    plt.close()

    #Proceso para graficar la curva 3D
    X, Y = np.meshgrid(xxmargin,yymargin)

    #Con el punto 2 se calcula la función de densidad acumulativa, se sustituyen los valores de los parámetros calculados
    zmargin = (1/(2*np.pi*19.88))*np.exp(-(X-9.905)**2/21.767 -(Y-15.08)**2/72.65)

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_wireframe(X, Y, zmargin, cmap=cm.coolwarm)
    ax.view_init(30, 35)
    ax.set_xlabel("Valores de X")
    ax.set_ylabel("Valores de Y")
    ax.set_zlabel("Probabilidad conjunta")
    ax.set_title("Función de densidad conjunta")
    plt.savefig("3dcurve.png")
    plt.show()

    #Se toman los valores del documento xyp.csv
    #Se asigna a x, y, p los valores de las respectivas columnas
    x = datos2.X
    y = datos2.Y
    p = datos2.P

    #Se calculan los momentos según la teoría
    covarianza_vector = (x-9.905)*(y-15.08)*p
    covarianza = sum(covarianza_vector)
    correlacion_vector = x*y*p
    correlacion = sum(correlacion_vector)
    pearson = covarianza/19.88
    
    print ("La covarianza es: ", covarianza)
    print ("La correlación es: ", correlacion)
    print ("El coeficiente de Pearson es: ", pearson)


#Se le asiga a los documentos una variable
file1 = "xy.csv"
file2 = "xyp.csv"

#Se utiliza pandas para poder manipular los datos de los respectivos documentos
datos1 = pd.read_csv(file1, skiprows=0, names=['y5','y6', 'y7', 'y8', 'y9', 'y10', 'y11', 'y12', 'y13', 'y14', 'y15', 'y16','y17', 'y18', 'y19', 'y20', 'y21', 'y22', 'y23', 'y24', 'y25'], header=0,)
datos2 = pd.read_csv(file2, skiprows=0, names=['X', 'Y', 'P'], header=0,)

#Se llama a la función
margin_dens(datos1, datos2, fx, xmargin, xxmargin, fy, ymargin, yymargin)