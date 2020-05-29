#Este elemento es creado por Willy barrios
from tkinter import ttk

from tkinter import *

import sqlite3

class contact:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Agenda de Contactos')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Registrar contacto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # num Input
        Label(frame, text = 'numero: ').grid(row = 2, column = 0)
        self.num = Entry(frame)
        self.num.grid(row = 2, column = 1)
        #

        # Button Add contacto 
        ttk.Button(frame, text = 'Guardar', command = self.add_contacto).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'black')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Numero', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'BORRAR', command = self.delete_contacto).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_contacto).grid(row = 5, column = 1, sticky = W + E)
        ttk.Button(frame, text = 'Info de la version',command = self.information).grid(row = 4,  columnspan = 2,sticky = W + E)
        ttk.Button(frame, text='Buscar', command =self.search).grid(row = 5,  columnspan = 2,sticky = W + E)
        # Filling the Rows
        self.get_names()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get names from Database
    def get_names(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM contacto ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling datad
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.num.get()) != 0

    def add_contacto(self):
        if self.validation():
            query = 'INSERT INTO contacto VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.num.get())
            self.run_query(query, parameters)
            self.message['text'] = 'contacto {} Agregado'.format(self.name.get())
            self.name.delete(0, END)
            self.num.delete(0, END)
        else:
            self.message['text'] = 'Nombre y numero requerido'
        self.get_names()

    def delete_contacto(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccionar correctamente el Item'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacto WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Contacto {} Eliminado'.format(name)
        self.get_names()

    def edit_contacto(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccionar correctamente el Item'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_num = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'EDITAR'
        # Old Name
        Label(self.edit_wind, text = 'Nombre Actual: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'Nombre Nuevo:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old num 
        Label(self.edit_wind, text = 'Numero Actual:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_num), state = 'readonly').grid(row = 2, column = 2)
        # New num
        Label(self.edit_wind, text = 'Numero Nuevo:').grid(row = 3, column = 1)
        new_num= Entry(self.edit_wind)
        new_num.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_num.get(), old_num)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_num, old_num):
        query = 'UPDATE contacto SET name = ?, num = ? WHERE name = ? AND num = ?'
        parameters = (new_name, new_num,name, old_num)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Contacto {} Actualizado'.format(name)
        self.get_names()
    def information(self):
        self.message['text']= '[version 1.0] in socials @R_Barrios_'
    def search(self):
        numero=self.num.get()
        if (numero==""):
          self.message['text']='Buscar","Inserta identificador'
        else:
            tupla=busca(numero)
            name.set(tupla[0])
            num.set(tupla[1])
            self.message['text']= 'Buscar","Contacto encontrado"'
        try:
            consulta.execute("SELECT * FROM contacto WHERE num="+str(numero))
            for i in consulta:
                name=i[1]
                num=i[2]
                return (name,num)
        except:
            self.message['text']= 'Buscar","Error al buscar'   

if __name__ == '__main__':
    window = Tk()
    application = contact(window)
    window.mainloop()
