'''
Created on 2017-01-22

@author: William Tchoudi
'''
import threading #
from threading import Event, Thread
from time import sleep
from pynput.keyboard import Key, Listener, Controller
import processText as pr
import claf # Clafrica code as literal objectfεte

''' global variable to store the keyboad sequence typed'''
strTyped = ""
''' global variable to Object Controller from pynput Module using to control the keyboad'''
keyType = Controller()
flag = False
trans = False
isRunning = True
proc = pr.ProcessText(claf.codeClafrica)

'''Method to get the the sequence of type characters from the keyboard and concat it as a string
the string is strored in a global variable in order to be read by different threads
@param key:Object Controller from pynput Module '''
def getCodeWords(key):
    global strTyped 
    global flag
    try:
        if (key == Key.space):
            
            strTyped += ' ' 
        elif (key == Key.backspace):
            #sleep(0.1)
            strTyped = strTyped[0:-1] 
        elif(len(format(key)[1:-1]) == 1):
            #sleep(0.1)
            strTyped += format(key)[1:-1] 
        elif(key == Key.enter):
            strTyped += '\n'
        else: #pass all snecial key not a character for example like ctl ...
            pass
    except  RuntimeError: 
        pass
    except  ValueError:
        pass


'''Override of the function on_press and on_release in order to match the getting keyboard character typed 
    thes function are used the keyboard Listner and run with'''
def on_press(key):
    if (key == Key.esc):
        #sys.exit()
        return False 
    pass
     
    #print(strTyped) 
def on_release(key):
    global trans
    getCodeWords(key)
    if (key == Key.space):
        #sys.exit()
        trans = True
        #return False   


class TranslateText(threading.Thread):
    '''
    This class extended from Thread Class set methods to get keyboard inputs using pynput Module
    '''
    global flag
    global trans
    global isRunning
    def __init__(self,procText,flashTime=0, gui=""):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.flashTime = flashTime # int interval time of second 
        self.procText = procText # Object ProcessText
        self.gui = gui
    def run(self): 
        global flag  
        global trans
        global isRunning
            #sleep(self.flashTimh   
        if (self.flashTime and self.gui == ""):
            while isRunning :
                if trans:
                    self.fireBackspace()
                    sleep(0.1)
                    trans = False
                    
            #self.setIntervalCall(self.flashTime,self.fireBackspace)  
        elif(not self.flashTime and self.gui == ""):
            
            with Listener(on_press=on_press,on_release=on_release) as listener:
                listener.join()
            #translate()
        elif (self.gui != "" and not self.flashTime):
            self.gui.guiLunch()
            
    '''Method to call in a given interval of second a call back method func passing it an argument as a pointer 
        @param interval:int 
        @param func:call back function  
        @param *arg:pointer of integer type to pass at the callback function func 
        @return: eventHandle.set an Event Object'''        
    def setIntervalCall(self,interval, func, *args):
        eventHandle = Event()
        def runRepeat():
            while not eventHandle.wait(interval): #wait the interval time before continue
                func(*args) # callback with argument 
        Thread(target=runRepeat).start()    
        return eventHandle.set
    
    ''' Method to remove the previous typed sequence of characters. This methos is call repeatidely in a thread'''   
    def fireBackspace(self):
        global flag
        global strTyped
        global keyType
        
        translateText = self.procText.getTranlate(strTyped) #get the translated text
        sp = ' '
        n = len(strTyped)
        strT = sp.join(strTyped.split())
        tabStr = strTyped.split('\n')
        nbSplit = len(tabStr)
          
        if(strTyped == ''):
            pass
        elif(strTyped == ' '):
            strT = ' '+ strT
            n = len(strT)
        if  flag: 
            for i in range(0,n + nbSplit -1):
                if (n != 0):
                    keyType.press(Key.backspace)
                    keyType.release(Key.backspace)
        
            for j in range(0,nbSplit):
                if (nbSplit == 1):
                    
                    keyType.type(translateText) # type the translated test in the current editing interface
                   
                else:
                    if(j != nbSplit-1):

                            translateText = self.procText.getTranlate(tabStr[j])
                            keyType.type(translateText)
                            keyType.press(Key.enter)
                            keyType.release(Key.enter)
                            
                    else:
                        translateText = self.procText.getTranlate(tabStr[j])
                        keyType.type(translateText)
                        #strTyped = '' 
        strTyped = '' 
#end
