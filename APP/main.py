from email.policy import default
from fileinput import filename
from tkinter import BOTTOM, DISABLED, HORIZONTAL, LEFT, NW, RIGHT, VERTICAL, X, Y, Checkbutton, Label, Spinbox, Tk, font, ttk, Frame, NORMAL, Text, Canvas
from tkinter.constants import TOP, BOTH
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno

from datetime import date, timedelta
from os.path import basename
from turtle import back

class App(Tk):
    def __init__(self):
        super().__init__()
        self.config_root()
        self.config_style()
        self.set_scrollbar()
        self.start_widgets()

    # ROOT   
    def config_root(self):
        self.resizable(width=False, height=False)
        self.geometry('1080x800')
        self.title("Movie Edit")
        self.main_color = '#eaeaf2'
        self.configure(background = self.main_color)
        
        self.left_side_widgets = {
            'buttons':[],
            'in':[],
            'out':[],
            'from':[],
            'to':[],
            'films':[]
        }
    
    # STYLE  
    def config_style(self):
        self.s = ttk.Style()
        self.s.configure('My.Label', background=self.main_color, font=('TkDefaultFont', 18))
        self.s.configure('TEntry', background='#ffffff', padding='10 10 10 10')        
        
    def set_scrollbar(self):
        def onCanvasConfigure(e):
            lutCanvas.itemconfig('frame', width=lutCanvas.winfo_width())
        
        lutCanvas = Canvas(self, background='#eaeaf2')
        scroll = ttk.Scrollbar(lutCanvas, orient=VERTICAL, command=lutCanvas.yview)
        self.write_frame = Frame(lutCanvas)
        
        lutCanvas.configure(yscrollcommand=scroll.set)
        lutCanvas.bind('<Configure>', lambda e: lutCanvas.configure(scrollregion=lutCanvas.bbox('all')))

        def _on_mouse_wheel(event):
            lutCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            
        lutCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        scroll.pack(side=RIGHT, fill=Y)
        lutCanvas.place(relheight=1, relwidth=0.4, relx=0)
        lutCanvas.create_window((0, 0), window=self.write_frame, anchor=NW, tags='frame')
        lutCanvas.bind("<Configure>", onCanvasConfigure)
        
        self.write_frame.columnconfigure(0, weight=1)       
        
        
    def start_widgets(self):   
        #LEFT SIDE WIDGETS
        #LABELS TOP
        Label(self.write_frame, text="Film", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=0)
        Label(self.write_frame, text="Od", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=1, columnspan=3)
        Label(self.write_frame, text=" ", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=4, columnspan=2)
        Label(self.write_frame, text="Do", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=6, columnspan=3)
        Label(self.write_frame, text=" ", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=9, columnspan=2)
        Label(self.write_frame, text="IN", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=11)
        Label(self.write_frame, text="OUT", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=12)
        
        #START BTN
        self.create_left_row()
        
        #RIGHT SIDE     
        #Labels
        ttk.Label(self, text='Tytuł:', style='My.Label').place(x=700, y=10)
        ttk.Label(self, text='Opis:', style='My.Label').place(x=700, y=100)
        ttk.Label(self, text='Miniaturka:', style='My.Label').place(x=700, y=300)
        
        #Entries
        self.titleEntry = ttk.Entry(self, style='TEntry', font=('TkDefaultFont', 14, 'bold'), width=30)
        self.descriptionEntry = Text(self, background='#ffffff', font=('TkDefaultFont', 14), width=30, height=6, padx=10, pady=10)
        
        #Button
        self.thBtn = ttk.Button(self, width=15, text='Wybierz...', command=self.button_min_click)
        
        self.place_widgets()
        
    def place_widgets(self):
        # LEFT INIT
        self.place_left_row(0)
        
        # RIGHT
        self.titleEntry.insert(0, ' - Dzika Gostomia cz. ***')
        self.titleEntry.place(x=700, y=45)
        self.descriptionEntry.place(x=700, y=135)
        self.thBtn.place(x=900, y=300)
        
    def create_left_row(self):
        self.left_side_widgets['buttons'].append(ttk.Button(self.write_frame, text='Wybierz film', command=self.button_film_click))
        self.left_side_widgets['from'].append((Spinbox(self.write_frame, from_=0, to=59, justify=RIGHT, width=2, font=('TkDefaultFont', 10)), Spinbox(self.write_frame, from_=0, to=59, width=2, justify=RIGHT, font=('TkDefaultFont', 10))))
        self.left_side_widgets['to'].append((Spinbox(self.write_frame, from_=0, to=59, justify=RIGHT, width=2, font=('TkDefaultFont', 10)), Spinbox(self.write_frame, from_=0, to=59, width=2, justify=RIGHT, font=('TkDefaultFont', 10))))
        self.left_side_widgets['in'].append(Checkbutton(self.write_frame))
        self.left_side_widgets['out'].append(Checkbutton(self.write_frame))
        
    def place_left_row(self, row_num):    
        self.left_side_widgets['buttons'][row_num].grid(row = row_num+1, column = 0)
        self.left_side_widgets['from'][row_num][0].grid(row = row_num+1, column=1)
        self.left_side_widgets['from'][row_num][1].grid(row = row_num+1, column=3)
        self.left_side_widgets['to'][row_num][0].grid(row = row_num+1, column=6)
        self.left_side_widgets['to'][row_num][1].grid(row = row_num+1, column=8)
        self.left_side_widgets['in'][row_num].grid(row = row_num+1, column = 11)
        self.left_side_widgets['out'][row_num].grid(row = row_num+1, column = 12)
        self.left_side_widgets['in'][row_num].select()
        self.left_side_widgets['out'][row_num].select()
        
        Label(self.write_frame, text=":", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = row_num+1, column=2)
        Label(self.write_frame, text=":", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = row_num+1, column=7)
        
        
    def button_min_click(self):
        self.thumbnailFileName = askopenfilename(filetypes=[("Images", "*.jpg")])
        if self.thumbnailFileName:
            self.thBtn.config(text=basename(self.thumbnailFileName))
        
    def button_film_click(self):
        self.create_left_row()
        self.place_left_row(len(self.left_side_widgets['buttons'])-1)
        
if __name__ == '__main__':
    App().mainloop()