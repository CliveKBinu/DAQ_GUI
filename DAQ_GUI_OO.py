from inspect import classify_class_attrs
from tkinter import *
from random import randint
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import PopupTimed, Window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
from ping3 import ping
import time
import threading

# constants


now = datetime.now()
current_time = now.strftime("%I:%M %p")

runNumber = 101 # change it 

NUM_DATAPOINTS = 10000 # only for the demo graph
dpts = [randint(0, 10) for x in range(NUM_DATAPOINTS)] # only for the demo graph

sleep_time = 5*60 # in seconds



#window Class
class startpage():


    def __init__(self):

        layout = [[sg.Text('Max Events',pad=(30,30)),sg.InputText(size=(50,50))],
              [sg.Button('Continuous Run',pad=(30,0)),sg.Button('Test Run',pad=(80,0))]]
        self.window1 = sg.Window('APDL DAQ GUI', layout,finalize=TRUE,size=(400,150)) # Finalize = True should be added so inorder to interaat with elements 






class Runmode_window():

    def __init__(self,runNumber,current_time,max_events,estimated_runtime):
        col_1 = [[sg.Text('Run Number:'),sg.Text(runNumber)],      
           [sg.Text('Run Start Time:'),sg.Text(current_time)],      
           [sg.Text('Events Recorded:'),sg.Text('Starting',key='Event_num')]]   

        col_2 = [[sg.Text('Emission File Directory:'),sg.Text("data_sets/run{}_{}.bin".format(runNumber,max_events))],   
           [sg.Text('Estimated Run Time:'),sg.Text(estimated_runtime)],      
           [sg.Text('Quanah Status:'),sg.Text('CHECKING',key='status')]]   

        # delete col_3 after implementing a way to move to next window       
        col_3 = [[sg.Button('Next')]]

        layout =[[sg.Column(col_1),sg.Column(col_2,pad=(30,0))],[sg.Column(col_3)]]
        
        self.window2 = sg.Window('RUN MODE', layout, finalize=True,size=(600,150),location=(800,150))
        window2 = self.window2
    
    # Ping starter and event counter

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


        def event_counter(window,max_events):
            i=0
            for k in range(max_events):
                window['Event_num'].update(k+1)
                time.sleep(5) # ask how the update works n try to link it into this 
                window.write_event_value('-THREAD2-',i)

    # Threading starts here:

        threading.Thread(target=ping_stat, args=(window2,
                            max_events,), daemon=True).start()

        threading.Thread(target=event_counter, args=(window2,max_events), daemon=True).start()


class runmode1():
    def __init__(self):
        layout = [[sg.Text('RUN XXX has successfully recorded')],[sg.Text("Quanah Upload Status:")],[sg.Text('Report Email Status:')]]
        self.window4 = sg.Window('runmode1',layout,finalize=True,size=(500,175))
        #window4 = self.window

        

class graph_window():
    def __init__(self):


        layout =[[sg.Radio('Muon rate','graph_radio',pad=(50,0),key="-IN-",enable_events=True),sg.Radio('Efficieny','graph_radio',key="-IN1-",enable_events=True),
        sg.Radio('Coincidence','graph_radio',pad=(50,0),key="-IN2-",enable_events=True)],
        [sg.Canvas(size=(640, 480), key='-CANVAS-')]]

        self.window3 = sg.Window('Graph Window', layout, finalize=True,size=(600,275),location=(100,150))
        window3 = self.window3
        canvas_elem = window3['-CANVAS-']
        canvas = canvas_elem.TKCanvas

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.grid()
        self.fig_agg = draw_figure(canvas, self.fig)



class Daqmode():
    def __init__(self):

        layout = [[sg.Text('RUN XXX has successfully recorded')],[sg.Text("Quanah Upload Status:")],[sg.Text('Report Email Status:')],[sg.Text('Wait Time Counter:')]]
        self.window5=sg.Window('Daqmode',layout,finalize=True,size=(500,175))
        #window5 = self.window

                
# draw figure function for graphing
    

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg




def main():
    a = startpage()
    window1 = a.window1
    while True:


        
        #try:
        window, event, values = sg.read_all_windows()
        #except TypeError:
         #   continue
    

        event1,values1 = window1.read()

        max_events = int(values1[0])
        estimated_runtime = max_events/(2*60)

        if event == sg.WIN_CLOSED:
            if window ==window1:
                break

     
        

        if event == 'Test Run':
            window2 = Runmode_window(runNumber,current_time,max_events,estimated_runtime).window2
            print('hello')
            window3 = graph_window().window3


 
        
    
        if event == '-IN-':
    
            for i in range(len(dpts)):
                event, values = window3.read(timeout=10)
                
                if event == 'Exit' or event == sg.WIN_CLOSED or event == '-IN1-' or event == '-IN2-' or event =='Next':
                    break
                graph_window().ax.cla()                  
                graph_window().ax.grid()                   
                data_points = int(45) 
                graph_window().ax.plot(range(data_points), dpts[i:i+data_points],  color='purple')
                graph_window().fig_agg.draw()
    


        if event == 'Next':
            window2.close()
            window3.close()
            #e = runmode1()
            window4 = runmode1().window4

        if event == 'Continuous Run':
            window5 = Daqmode().window5

        

        #window.close()
if __name__ == '__main__':
    main()
    