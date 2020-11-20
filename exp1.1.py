import tkinter
from tkinter.filedialog import *

displayed_time = None


def open_file_dialog() :
    global displayed_time 
    
    
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if len(in_filename) == 0 :
        print("empty")
    else :
        print("kapra")
        displayed_time.set("0")   
        print(displayed_time.get())
    




def main() :
    
    global displayed_time

    root = tkinter.Tk()
   
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    b = 198

    

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    
    a = tkinter.StringVar()
    a.set(str(b) + "lul")
    
    displayed_time = tkinter.StringVar()
    displayed_time.set(str(b) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    

    root.mainloop()
    print('Modelling finished!')

main()