from tkinter import *
from keyboard_thread import Concur
'''
Created on 2017-01-22
@author: William Tchoudi, Harvey Sama
Main file to call all module and run the program
'''

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
        self.concur = None

    ''' Method to build a simple graphical interface that allow to  to start and stop the clafrica '''
    def guiLunch(self):
        root = Tk()
        root.title("Clafrica all lane")
        root.geometry("440x380")
        app = Frame(root)
        photo = PhotoImage(file="logo.png")
        app.grid()
        img = Label(app, image=photo)

        '''Method that start the clafica to fire translation when type clafica code  '''
        def startClafica():
            self.concur = Concur()
            self.concur.start()
            startBut.config(state="disabled", bg='yellow')

        ''' Method stopClafrica to stop the Clafrica and close the GUI'''
        def stopClafrica():
            startBut.config(state="normal", bg='green')
            self.concur.pause()
        ''' internal function onClose to handle close window event on callback'''
        def onClose():

            # self.concur.stop()
            root.destroy()   # stops the main loop
            sys.exit(1)

        startBut = Button(app, text="Start Clafrica", width=15, height=2 , bg='green', fg = 'white', command = startClafica)
        stopBut = Button(app, text="Stop Clafrica", width=15, height=2, bg='red', fg = 'white', command = stopClafrica)
        clafricaLabel = Label(app, text="This Clafrica allow you to translate your Clafrica Code when editing \n \
        For a complete text translation use the online Version at:\n http://resulam.com/fr/clafrica-web/\n \
        Press Start Button to start the application and stop Button to stop Clafrica \n \
        To exit the whole application simply close the Window")

        emptyText = Label(app, text="  ")
        img.grid()
        clafricaLabel.grid(row=2, column=0)
        startBut.grid(column=0, row=3)
        emptyText.grid(row=4, column=0)
        stopBut.grid(column=0, row=5)

        root.bind('<Escape>', lambda e: root.destroy())
        root.protocol("WM_DELETE_WINDOW", onClose)  # handle event when window is closed by user
        root.resizable(width=False, height=False)
        root.mainloop()

if __name__ == '__main__':
    gui = GuiHandle()
    gui.guiLunch()
