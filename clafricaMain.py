# coding: utf-8 
'''
Created on 2017-01-22

@author: William Tchoudi
Main file to call all module and run the program
'''
from tkinter import * 
import processText as pr
import translateText as tr
import claf # Clafrica code as literal object


class GuiHandle():
    '''
    This class handle the graphical interface view with the start and stop Button  
    start button  run the program and stop button stop it 
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        global flag
        global isRunning 
    
    ''' Method to build a simple graphical interface that allow to  to start and stop the clafrica '''
    def guiLunch(self):
        root = Tk()
        root.title("Clafrica all lane")
        root.geometry("500x350")
        app = Frame(root)
        photo = PhotoImage(file="logo.png")
        app.grid()
        img = Label(app, image=photo)
        '''Method that start the clafica to fire translation when type clafica code  '''
        def startClafica():     
            """Enable start thead  by setting the global flag to True."""
            global flag
            tr.flag = True
        ''' Method stopClafrica to stop the Clafrica and close the GUI'''
        def stopClafrica():
            """Stop program and set the global flag to False."""
            global keyType
            global flag
            tr.flag = False
        ''' internal function onClose to handle close window event on callback''' 
        def onClose():
            """Stop program and set the global flag to False."""
            global keyType
            global isRunning 
            stopClafrica()
            tr.keyType.press(tr.Key.esc)
            tr.keyType.release(tr.Key.esc)
            tr.isRunning = False
            root.destroy()   # stops the main loop
            sys.exit(1)
        
        startBut = Button(app, text="Start Clafrica", width=15, height=2 , bg='green', fg = 'white', command = startClafica)
        stopBut = Button(app, text="Stop Clafrica", width=15, height=2, bg='red', fg = 'white', command = stopClafrica)
        clafricaLabel = Label(app, text="This Clafrica allow you to \n translate your Clafrica Code when editing \n for a complete text translation use the online Version at:\n http://resulam.com/fr/clafrica-web/\n Press Start Button to start the application and stop Button to stop Clafrica \n To exit the whole application simply close the Window")
        emptyText = Label(app, text="  ")
        img.grid()
        clafricaLabel.grid(row = 2, column = 0)
        startBut.grid(column=0,row=3)
        emptyText.grid(row = 4 , column = 0)
        stopBut.grid(column=0,row=5)
    
    
        root.bind('<Escape>', lambda e: root.destroy())
        root.protocol("WM_DELETE_WINDOW", onClose)  # handle event when window is closed by user 
        root.mainloop() 

def main():
    proc = pr.ProcessText(claf.codeClafrica)
    thread1 = tr.TranslateText(proc,6)
    thread2 = tr.TranslateText(proc)
    thread1.daemon=True #making deamon to close the close it when the main threat is finished
    thread2.daemon=True
    gui = GuiHandle()
    thread3 = tr.TranslateText(proc,0,gui)
    thread3.daemon=True
    try:
        thread3.start()
        thread1.start()
        thread2.start()
        thread3.join()
        thread1.join()
        thread2.join()
    finally: 
        sys.exit(1)
main() 