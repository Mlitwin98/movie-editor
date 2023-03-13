from tkinter import  HORIZONTAL, NW, RIGHT, VERTICAL, Y, Checkbutton, IntVar, Label, Spinbox, Tk, Frame, ttk, Canvas, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename

import ttkbootstrap as ttkb

from os.path import basename

from threading import Thread
from tkinter.messagebox import askyesno
from editor import Editor

from moviepy.editor import VideoFileClip

from settings import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.config_root()
        self.config_style()
        self.set_scrollbar()
        self.start_widgets()

    # ROOT   
    def config_root(self):
        """
            Root settings:\n
            Is not resizable\n
            Set geometry\n
            Set title\n
            Set background color
        """
        self.resizable(width=False, height=False)
        self.geometry(GEOMETRY)
        self.title(TITLE)
        self.main_color = MAIN_COLOR
        #self.configure(background = self.main_color)
    
    # STYLE  
    def config_style(self):
        """
            Config default styles
        """
        self.s = ttkb.Style('superhero')
        self.s.configure('My.Label', font=('TkDefaultFont', 18))
        self.s.configure('TEntry', background='#ffffff', padding='10 10 10 10')        
        
    def set_scrollbar(self):
        """
            Config left side scrollbar
        """
        def onCanvasConfigure(e):
            lutCanvas.itemconfig('frame', width=lutCanvas.winfo_width())
        
        lutCanvas = Canvas(self)
        self.write_frame = Frame(lutCanvas)
        
        scroll = ttk.Scrollbar(self.write_frame, orient=VERTICAL, command=lutCanvas.yview, bootstyle='light-round')
        
        lutCanvas.configure(yscrollcommand=scroll.set)
        lutCanvas.bind('<Configure>', lambda e: lutCanvas.configure(scrollregion=lutCanvas.bbox('all')))

        def _on_mouse_wheel(event):
            lutCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            
        lutCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        lutCanvas.place(relheight=1, relwidth=0.6, relx=-0.005)
        lutCanvas.create_window((0, 0), window=self.write_frame, anchor=NW, tags='frame')
        lutCanvas.bind("<Configure>", onCanvasConfigure)
        
        self.write_frame.columnconfigure(0, weight=1)     
        
        self.reset_data()   
        
        
    def start_widgets(self):
        """
            Initialize statick widgets and create 1st left row
        """ 
        #LEFT SIDE WIDGETS
        #LABELS TOP
        Label(self.write_frame, text="Film", height=3, font=TOP_FONT).grid(row = 0, column=0)
        Label(self.write_frame, text="Od", height=3, font=TOP_FONT).grid(row = 0, column=1, columnspan=3)
        Label(self.write_frame, text=" ", height=3, font=TOP_FONT).grid(row = 0, column=4, columnspan=2)
        Label(self.write_frame, text="Do", height=3, font=TOP_FONT).grid(row = 0, column=6, columnspan=3)
        Label(self.write_frame, text=" ", height=3, font=TOP_FONT).grid(row = 0, column=9, columnspan=2)
        Label(self.write_frame, text="IN", height=3, font=TOP_FONT).grid(row = 0, column=11)
        Label(self.write_frame, text="OUT", height=3, font=TOP_FONT).grid(row = 0, column=12)
        
        #START BTN
        self.create_left_row()
        
        #RIGHT SIDE     
        #Labels
        ttkb.Label(self, text='INTRO:', style='My.Label').place(INTRO_PLACEMENT)
        ttkb.Label(self, text='OUTRO:', style='My.Label').place(OUTRO_PLACEMENT)
        
        #Check Boxes
        self.intro_var = IntVar(value=1)
        self.outro_var = IntVar(value=1)
        self.intro_check = ttkb.Checkbutton(self, variable=self.intro_var, bootstyle="success-round-toggle")
        self.outro_check = ttkb.Checkbutton(self, variable=self.outro_var, bootstyle="success-round-toggle")
        
        #Button
        self.textBtn = ttkb.Button(self, width=20, text='Dodaj napis', command=self.add_text, bootstyle='primary')
        self.renderBtn = ttkb.Button(self, width=20, text='Render', command=self.render, bootstyle='success')
        self.resetBtn = ttkb.Button(self, width=10, text='RESET', command=self.reset, bootstyle='danger')
        
        #Progress Bar
        self.pb = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate', length=300, bootstyle="success-striped")
        
        self.place_widgets()
        
    def place_widgets(self):
        """
            Place initialized statick widgets
        """
        # LEFT INIT
        self.place_left_row(0)
        
        # RIGHT
        self.intro_check.place(INTRO_CHECK_PLACEMENT)
        self.outro_check.place(OUTRO_CHECK_PLACEMENT)
        self.textBtn.place(ADD_TEXT_PLACEMENT)
        self.resetBtn.place(RESET_PLACEMENT)
        self.renderBtn.place(RENDER_PLACEMENT)
        
        self.pb.place(PROGRESSBAR_PLACEMENT)
        
    def create_left_row(self, dur_min:int=0, dur_sec:int=0, text_button:bool=False) -> int:
        """
            Initialize additional left row

        Args:
            dur_min (int, optional): Duration minutes to set the spinxbox to. Defaults to 0.
            dur_sec (int, optional): Duration seconds to set the spinbox to. Defaults to 0.
            text_button (bool, optional): Should added row be with text button. Defaults to False.

        Returns:
            int: Created row number, counting from 1
        """
        row = len(self.left_side_widgets['buttons'])
        if text_button:
            self.left_side_widgets['buttons'].append(ttkb.Button(self.write_frame, text='Napisz tekst', command= lambda i=row: self.button_text_click(i)))
        else:
            self.left_side_widgets['buttons'].append(ttkb.Button(self.write_frame, text='Wybierz film', command= lambda i=row: self.button_film_click(i)))
        self.left_side_widgets['from'].append((Spinbox(self.write_frame, from_=0, to=59, justify=RIGHT, width=4, font=('TkDefaultFont', 10)), Spinbox(self.write_frame, from_=0, to=59, width=4, justify=RIGHT, font=('TkDefaultFont', 10))))
        self.left_side_widgets['to'].append((Spinbox(self.write_frame, from_=0, to=59, justify=RIGHT, width=4, font=('TkDefaultFont', 10)), Spinbox(self.write_frame, from_=0, to=59, width=4, justify=RIGHT, font=('TkDefaultFont', 10))))
        self.left_side_widgets['in'].append(ttkb.Checkbutton(self.write_frame, variable=IntVar(value=1), bootstyle="success-round-toggle"))
        self.left_side_widgets['out'].append(ttkb.Checkbutton(self.write_frame, variable=IntVar(value=1), bootstyle="success-round-toggle"))
        self.left_side_widgets['placeholders'].append((Label(self.write_frame, text=":", height=3, font=('TkDefaultFont', 14, 'bold')), Label(self.write_frame, text=":", height=3, font=('TkDefaultFont', 14, 'bold'))))
        self.left_side_widgets['delete'].append(ttkb.Button(self.write_frame, width=1, text='X', command= lambda i=row: self.delete_row(i), bootstyle='danger'))
        self.set_spinboxes(row, dur_min=dur_min, dur_sec=dur_sec)
        return row
        
    def place_left_row(self, row_num): 
        """
            Place additional left row
        
        Args:
            row_num (int): Row to place
        """   
        self.left_side_widgets['buttons'][row_num].grid(row = row_num+1, column = 0)
        self.left_side_widgets['from'][row_num][0].grid(row = row_num+1, column=1)
        self.left_side_widgets['from'][row_num][1].grid(row = row_num+1, column=3)
        self.left_side_widgets['to'][row_num][0].grid(row = row_num+1, column=6)
        self.left_side_widgets['to'][row_num][1].grid(row = row_num+1, column=8)
        self.left_side_widgets['in'][row_num].grid(row = row_num+1, column = 11)
        self.left_side_widgets['out'][row_num].grid(row = row_num+1, column = 12)
        self.left_side_widgets['delete'][row_num].grid(row = row_num+1, column = 13)
        
        self.left_side_widgets['placeholders'][row_num][0].grid(row = row_num+1, column=2)
        self.left_side_widgets['placeholders'][row_num][1].grid(row = row_num+1, column=7)
        
    def delete_row(self, row:int, single:bool=True):
        """
            Delete specified row

        Args:
            row (int): Row to delete
            single (bool, optional): If deletion operation is done on one or all rows. Defaults to True.
        """
        self.left_side_widgets['delete'][row].destroy()
        self.left_side_widgets['buttons'][row].destroy()
        self.left_side_widgets['in'][row].destroy()
        self.left_side_widgets['out'][row].destroy()
        self.left_side_widgets['from'][row][0].destroy()
        self.left_side_widgets['from'][row][1].destroy()
        self.left_side_widgets['to'][row][0].destroy()
        self.left_side_widgets['to'][row][1].destroy()
        self.left_side_widgets['placeholders'][row][0].destroy()
        self.left_side_widgets['placeholders'][row][1].destroy()
          
        if single:
            try:      
                self.left_side_widgets['films'][row] = None
            except:
                self.left_side_widgets['films'].append(None)
                
    def set_spinboxes(self, row:int, dur_min:int, dur_sec:int):
        """
        Edit "to" spinbox in specified row to specified minutes and seconds

        Args:
            row (int): Spinbox row to edit
            dur_min (int): Duration minutes to set
            dur_sec (int): Duration seconds to set
        """
        self.left_side_widgets['to'][row][0].delete(0, 'end')
        self.left_side_widgets['to'][row][0].insert(0, dur_min)
        
        self.left_side_widgets['to'][row][1].delete(0, 'end')
        self.left_side_widgets['to'][row][1].insert(0, dur_sec)
    
    def reset(self):
        """
            Reset left side
        """
        answer = askyesno(title='POTWIERDŹ', message=f'CZY NA PEWNO CHCESZ ZRESETOWAĆ WIDOK?')
        if answer: 
            for i in range(len(self.left_side_widgets['buttons'])):
                self.delete_row(i, single=False)
            
            self.reset_data()
            
            self.create_left_row()
            self.place_left_row(0)
        
    def reset_data(self):
        """
            Reset stored film variables
        """
        self.left_side_widgets = {
                'delete':[],
                'buttons':[],
                'in':[],
                'out':[],
                'from':[],
                'to':[],
                'placeholders':[],
                'films':[]
            } 

    def button_text_click(self, row:int):
        """
            Change text of text button in specified row

        Args:
            row (int): Row in which to change button's text in
        """
        if len(self.left_side_widgets['films']) > row:
            text = simpledialog.askstring(f'Tekst', 'Wprowadź tekst:\t\t\t\t\t\t\t\t\t\t\t', initialvalue=self.left_side_widgets['films'][row])
            self.left_side_widgets['films'][row] = text
        else:
            text = simpledialog.askstring(f'Tekst', 'Wprowadź tekst:\t\t\t\t\t\t\t\t\t\t\t')
            self.left_side_widgets['buttons'][row].config(text='Tekst')  
            self.left_side_widgets['films'].append(text)
            new_row = self.create_left_row()
            self.set_spinboxes(row, dur_min=0, dur_sec=6)
            self.place_left_row(new_row)
        
    def add_text(self):
        """
            Add text button
        """
        row = self.create_left_row(text_button=True)
        self.place_left_row(row)
        
    def button_film_click(self, row:int):
        """
            Asks for file and add it to clips or change existing

        Args:
            row (int): Row in which button was clicked
        """
        film_name = askopenfilename(filetypes=[("Movie", 
                                                    "*.mp4 *.mkv *.flv *.webm *.avi *.wmv *.mpg *.mpeg *.flv *.mov *.mts"
                                                    )])
        if film_name != '':
            self.left_side_widgets['buttons'][row].config(text=basename(film_name))
            
            vid = VideoFileClip(film_name)
            duration = int(vid.duration)
            
            dur_min = duration//60
            dur_sec = duration - dur_min*60
            
            self.set_spinboxes(row, dur_min=dur_min, dur_sec=dur_sec)
            
            if len(self.left_side_widgets['films']) > row:
                self.left_side_widgets['films'][row] = film_name
            else:
                self.left_side_widgets['films'].append(film_name)
                new_row = self.create_left_row()
                self.place_left_row(new_row)
    
    def render(self):
        """
            Asks user for path and filename of rendered movie\n
            Creates Editor in new thread based on given left side variables
        """
        directory = asksaveasfilename(defaultextension=".mp4", filetypes=[('Movie', '*.mp4')])
        if directory is not None and len(directory) > 0:
            out = []
            for i, film in enumerate(self.left_side_widgets['films']):
                if film is not None:
                    state_in = self.left_side_widgets['in'][i].state()
                    state_out = self.left_side_widgets['out'][i].state()
                    
                    semi = {}
                    semi['film'] = film
                    semi['from'] = int(self.left_side_widgets['from'][i][0].get()) * 60 + int(self.left_side_widgets['from'][i][1].get())
                    semi['to'] = int(self.left_side_widgets['to'][i][0].get()) * 60 + int(self.left_side_widgets['to'][i][1].get())
                    semi['in'] = 'selected' in state_in or 'alternate' in state_in
                    semi['out'] = 'selected' in state_out or 'alternate' in state_out
                    semi['is_text'] = True if self.left_side_widgets['buttons'][i]['text'] == 'Tekst' else False

                    out.append(semi)
                
            self.editor = Editor(out, self.intro_var.get(), self.outro_var.get(), directory, self.pb, self.renderBtn)
            
            tr = Thread(target = self.editor.edit) 
            tr.start()
        
if __name__ == '__main__':
    App().mainloop()