from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import sqlite3
# from kivy.core.window import Window
# Window.size=(1520,720)

class main_app(MDApp):
          
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        #create database or connect to one
        conn = sqlite3.connect('D:/projectpython/first_db.db')

        #create a cursor
        c = conn.cursor()
         
        #create a Table
        c.execute("""CREATE TABLE if not exists users(
            username text,
            password text
        )
        """)
        #commit our changes
        conn.commit()

        #close our connction
        conn.close()

        return Builder.load_file("acounte_style.kv")  
    
    def login(self):
        #create database or connect to one
        conn = sqlite3.connect('D:/projectpython/first_db.db')

        #create a cursor
        c = conn.cursor()
        
        #add a user
        in_user = f'{self.root.ids.user.text}' 
        in_pas = f'{self.root.ids.pswrd.text}'
        query = f"SELECT * FROM users WHERE username='{in_user}'"
      

        c.execute(query)
          
        cheakee=True
        if in_pas.isalpha() or in_pas.isdigit() or len(list(in_pas))<8:
            cheakee=False
        records = c.fetchall()
        print(records);
        # print(type(records))
        if(len(records) == 0 and in_user.find("@gmail.com")>0 and cheakee ):

            if (in_user != "" and in_pas != ""):
                

                c.execute("INSERT INTO users VALUES(?,?)",(in_user,in_pas))

                #add a litter masseg
                # self.root.ids.wellcome_lb.text=f'{self.root.ids.user.text} added'

                # clear the input box 
                self.root.ids.user.text = ".mm."
                self.root.ids.pswrd.text = ""
                
        #commit our changes
        conn.commit()

        #close our connction
        conn.close()
        self.reLoad()

    def reLoad(self):
        #create database or connect to one
        conn = sqlite3.connect('D:/projectpython/first_db.db')

        #create a cursor
        c = conn.cursor()
        
        c.execute("SELECT * FROM users")

        records = c.fetchall()
      
        #commit our changes
        conn.commit()

        #close our connction
        conn.close()

        #_______________________

         # define datatables
        table = MDDataTable(
            size_hint=(0.9,0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check = True,
            use_pagination = True,
            rows_num = 8,
            pagination_menu_height = "240dp",
            pagination_menu_pos = "auto",
            
            column_data = [
                ("users", dp(50)),
                ("password", dp(30)),
                
                
            ],
            row_data = [
                (f'{record[0]}',f'{record[1]}') for record in records],
        )
        table.bind(
            on_check_press = self.checked,
            on_row_press = self.row_check
        )

        
        # add widget to screen
        self.root.ids.flut.add_widget(table)
        
    def checked(self, instance_table, current_row):
        pass
    def row_check(self, instance_table,row):
        # defined the postion in table such as array 
        start_index , end_index = row.table.recycle_data[row.index]['range']
        #print(start_index)
        #print(end_index)

        #print all index in row
        #for i in range(start_index, end_index+1):
            #print(row.table.recycle_data[i]['text'])
            
        # put data in textbox
        self.root.ids.user.text = row.table.recycle_data[start_index]['text']
        self.root.ids.pswrd.text = row.table.recycle_data[end_index]['text']
    def update(self):
        conn = sqlite3.connect('D:/projectpython/first_db.db')

        #create a cursor
        c = conn.cursor()
        
        _user = f'{self.root.ids.user.text}' 
        _pas = f'{self.root.ids.pswrd.text}'

        c.execute(" UPDATE users SET password=? WHERE username=? ",(_pas,_user))

        conn.commit()
        conn.close()
        self.reLoad()
        
    def delete(self):
        conn = sqlite3.connect('D:/projectpython/first_db.db')

        #create a cursor
        c = conn.cursor()
        
        d_user = f'{self.root.ids.user.text}' 
        d_pas = f'{self.root.ids.pswrd.text}'

        c.execute(" DELETE FROM users WHERE username=? AND password=? ",(d_user,d_pas))

        conn.commit()
        conn.close()
        self.root.ids.user.text = ""
        self.root.ids.pswrd.text = ""
        self.reLoad()
        
    def on_start(self, **kwargs):
        self.reLoad()

main_app().run()