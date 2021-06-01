from tkinter import *
from random import randint
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Graph, Print
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import tkinter as Tk
import matplotlib.pyplot as plt
import timeit


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


NUM_DATAPOINTS = 10000
dpts = [randint(0, 10) for x in range(NUM_DATAPOINTS)]

def startpage():
    layout = [[sg.Text('Max Events',pad=(30,30)),sg.InputText(size=(50,50))],
              [sg.Button('Continuous Run',pad=(30,0)),sg.Button('Test Run',pad=(80,0))]]
    window = sg.Window('APDL DAQ GUI', layout,finalize=TRUE,size=(400,150)) # Finalize = True should be added so inorder to interaat with elements 
    #event,values = window.read()
    #max_events = int(values[0])
    #estimated_runtime = max_events/(2*60)
    return window


def Runmode():
    
    col_1 = [[sg.Text('Run Number:')],      
           [sg.Text('Run Start Time:')],      
           [sg.Text('Events Recorded:')]]   

    col_2 = [[sg.Text('Emission File Directory:')],      
           [sg.Text('Estimated Run End Time:'),sg.Text(estimated_runtime)],      
           [sg.Text('Quanah Status:')]]   

    # delete col_3 after implementing a way to move to next window       
    col_3 = [[sg.Button('Next')]]

    layout =[[sg.Column(col_1),sg.Column(col_2,pad=(70,0))],[sg.Column(col_3)],
            [sg.Radio('Muon rate','graph_radio',pad=(50,0),key="-IN-",enable_events=True),sg.Radio('Efficieny','graph_radio',key="-IN1-",enable_events=True),
            sg.Radio('Coincidence','graph_radio',pad=(50,0),key="-IN2-",enable_events=True)],
            [sg.Canvas(size=(640, 480), key='-CANVAS-')]]

    window = sg.Window('RUN MODE', layout, finalize=True,size=(500,375))
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()
    fig_agg = draw_figure(canvas, fig)

    #graph = window['graph']
    return window,canvas,ax,fig_agg,fig

def runmode1():
    layout = [[sg.Text('RUN XXX has successfully recorded')],[sg.Text("Quanah Upload Status:")],[sg.Text('Report Email Status:')]]
    return sg.Window('runmode1',layout,finalize=True,size=(500,175))
    

def Daqmode():
    layout = [[sg.Text('RUN XXX has successfully recorded')],[sg.Text("Quanah Upload Status:")],[sg.Text('Report Email Status:')],[sg.Text('Wait Time Counter:')]]
    return sg.Window('Daqmode',layout,finalize=True,size=(500,175))



window1 = startpage() #starting the first page   

while True:            

    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED:
        if window == window1:
            break
        #except AttributeError:
         #  pass

    try:
        event1 , values1 = window1.read(timeout=10)
        max_events = int(values1[0])
        print(max_events)
    except TypeError:
        pass

    estimated_runtime = max_events/(2*60)
  
    if event == 'Test Run':
        window2,canvas,ax,fig_agg,fig = Runmode()
        window2.bring_to_front()
    
    if event == 'Next':
        window2.close()
        print('hello')
        window3 = runmode1()
        window3.bring_to_front()


    if event == '-IN-':

        # replace this with the nesscary code


        for i in range(len(dpts)):
            event, values = window2.read(timeout=10)
            
            if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN1-' or event == '-IN2-':
                break
            ax.cla()                  
            ax.grid()                   
            data_points = int(45) 
            ax.plot(range(data_points), dpts[i:i+data_points],  color='purple')
            fig_agg.draw()
                
    if event =='-IN1-':

        for i in range(len(dpts)):
            event, values = window2.read(timeout=10)
            if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN-' or event == '-IN2-':
                break
            ax.cla()                  
            ax.grid()                   
            data_points = int(45) 
            ax.plot(range(data_points), dpts[i:i+data_points],  color='red')
            fig_agg.draw()



    if event =='-IN2-':


        for i in range(len(dpts)):
            event, values = window2.read(timeout=10)
            if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN-' or event == '-IN1-':
                break
            ax.cla()                  
            ax.grid()                   
            data_points = int(45) 
            ax.plot(range(data_points), dpts[i:i+data_points],  color='green')
            fig_agg.draw()
        

    if event == 'Continuous Run':
        #window1.close()
        window4 = Daqmode()
        window4.bring_to_front()

window.close()
