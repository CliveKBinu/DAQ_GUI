from tkinter import *
from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
from ping3 import ping
import time
import threading



now = datetime.now()
current_time = now.strftime("%I:%M %p")

runNumber = 101 # change it 

NUM_DATAPOINTS = 10000 # only for the demo graph
dpts = [randint(0, 10) for x in range(NUM_DATAPOINTS)] # only for the demo graph


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def ping_stat(window,max_events):
    #t_end = time.time() + estimated_runtime
    i=0

    #while time.time() < t_end:
    for i in range(max_events):
        a = ping('8.8.8.8')
        if a != None:
            window['status'].update('UP',text_color='Green')
            print('Up')
        else:
            window['status'].update('DOWN',text_color='red')
            print('down')
        time.sleep(3)

        i+=1
        print(i)
        window.write_event_value('-THREAD1-',i)



def event_counter(window):
    i=0
    for k in range(max_events):
        window['Event_num'].update(k+1)
        time.sleep(3) # ask how the update works n try to link it into this 
        window.write_event_value('-THREAD2-',i)






def startpage():
    layout = [[sg.Text('Max Events',pad=(30,30)),sg.InputText(size=(50,50))],
              [sg.Button('Continuous Run',pad=(30,0)),sg.Button('Test Run',pad=(80,0))]]
    window = sg.Window('APDL DAQ GUI', layout,finalize=TRUE,size=(400,150)) # Finalize = True should be added so inorder to interaat with elements 

    return window



def Runmode():
    
    col_1 = [[sg.Text('Run Number:'),sg.Text(runNumber)],      
           [sg.Text('Run Start Time:'),sg.Text(current_time)],      
           [sg.Text('Events Recorded:'),sg.Text('Starting',key='Event_num')]]   

    col_2 = [[sg.Text('Emission File Directory:'),sg.Text("data_sets/run{}_{}.bin".format(runNumber,max_events))],   
           [sg.Text('Estimated Run Time:'),sg.Text(estimated_runtime)],      
           [sg.Text('Quanah Status:'),sg.Text('CHECKING',key='status')]]   

    # delete col_3 after implementing a way to move to next window       
    col_3 = [[sg.Button('Next')]]

    layout =[[sg.Column(col_1),sg.Column(col_2,pad=(30,0))],[sg.Column(col_3)]]

    window = sg.Window('RUN MODE', layout, finalize=True,size=(600,150),location=(800,150))

    thread_id = threading.Thread(target=ping_stat, args=(window,max_events,), daemon=True)
    thread_id2 = threading.Thread(target=event_counter, args=(window,), daemon=True)
    thread_id.start()
    thread_id2.start()

    return window


def graph_window():
    layout =[[sg.Radio('Muon rate','graph_radio',pad=(50,0),key="-IN-",enable_events=True),sg.Radio('Efficieny','graph_radio',key="-IN1-",enable_events=True),
            sg.Radio('Coincidence','graph_radio',pad=(50,0),key="-IN2-",enable_events=True)],
            [sg.Canvas(size=(640, 480), key='-CANVAS-')]]

    window = sg.Window('Graph Window', layout, finalize=True,size=(600,275),location=(100,150))
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

    try:
        window, event, values = sg.read_all_windows()
    except TypeError:
        continue

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
        window2 = Runmode()
        window3,canvas,ax,fig_agg,fig = graph_window()
        window2.bring_to_front()
        window3.bring_to_front()



        
  
    if event == '-IN-':

    

    
        for i in range(len(dpts)):
            event, values = window3.read(timeout=10)
            
            if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN1-' or event == '-IN2-' or event=='Next':
                break
            ax.cla()                  
            ax.grid()                   
            data_points = int(45) 
            ax.plot(range(data_points), dpts[i:i+data_points],  color='purple')
            fig_agg.draw()
                
    if event =='-IN1-':

        for i in range(len(dpts)):
            event, values = window3.read(timeout=10)
            if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN-' or event == '-IN2-' or event=='Next':
                break
            ax.cla()                  
            ax.grid()                   
            data_points = int(45) 
            ax.plot(range(data_points), dpts[i:i+data_points],  color='red')
            fig_agg.draw()



    if event =='-IN2-':


        for i in range(len(dpts)):
            event, values = window3.read(timeout=10)
            if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN-' or event == '-IN1-' or event=='Next':
                break
            ax.cla()                  
            ax.grid()                   
            data_points = int(45) 
            ax.plot(range(data_points), dpts[i:i+data_points],  color='green')
            fig_agg.draw()


    if event == 'Next':
        window2.close()
        window3.close()
        #print('hello')
        window4 = runmode1()
        window4.bring_to_front()
    

    if event == 'Continuous Run':
        #window1.close()
        window5 = Daqmode()
        window5.bring_to_front()

window.close()
