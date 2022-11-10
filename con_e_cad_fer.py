#Importando o Tkinter

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox,Treeview
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from tkinter import messagebox
import sqlite3
import webbrowser


janela = Tk()

class Validadores():
    def validate_entryPart(self, text):
        if text == "":
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <=99999
    def validate_entryCodigo(self, text):
        if text == "":
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 99999
    def validate_Textos(self, text):
        if text.isdigit():
            return True
        elif text == "":
            return True
        else:
            return False


class Relatorios():
    def printTec(self):
        webbrowser.open("cadastroTec.pdf")
    def geraRelatTec(self):
        self.c = canvas.Canvas("cadastroTec.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.e_nome.get()
        self.cpfRel = self.e_cpf.get()
        self.telefoneRel = self.e_telefone.get()
        self.equipeRel = self.e_equipe.get()
        self.turnoRel = self.e_turno.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, "Ficha dos Técnicos")

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, "Codigo: ")
        self.c.drawString(50, 670, "Nome: ")
        self.c.drawString(50, 640, "CPF: ")
        self.c.drawString(50, 610, "Telefone: ")
        self.c.drawString(50, 580, "Equipe: ")
        self.c.drawString(50, 550, "Turno: ")

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 640, self.cpfRel)
        self.c.drawString(150, 610, self.telefoneRel)
        self.c.drawString(150, 580, self.equipeRel)
        self.c.drawString(150, 550, self.turnoRel)

        self.c.rect(20, 530, 550, 1, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.printTec()

class Funcs:
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.e_part_number.delete(0, END)
        self.e_fabricante.delete(0, END)
        self.e_tamanho.delete(0, END)
        self.e_medida.delete(0, END)
        self.e_volts.delete(0, END)
        self.e_tipo.delete(0, END)
        self.e_material.delete(0, END)
        self.e_descricao.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("cadastroFerramenta.bd")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):
        self.conn.close()
    def montaTabelas(self):
        self.conecta_bd()
        print("Conectando ao banco de dados")
        # Criar tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ferramentas (
                                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                                part_number INTEGER NOT NULL,
                                fabricante TEXT NOT NULL,
                                volts TEXT NOT NULL,
                                tamanho INTEGER NOT NULL,
                                medida TEXT NOT NULL,
                                tipo TEXT NOT NULL,
                                material TEXT NOT NULL,
                                descricao TEXT NOT NULL
                                );""")
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()
    def variavel(self):
        self.codigo = self.codigo_entry.get()
        self.part_number = self.e_part_number.get()
        self.fabricante = self.e_fabricante.get()
        self.tamanho = self.e_tamanho.get()
        self.medida = self.e_medida.get()
        self.volts = self.e_volts.get()
        self.tipo = self.e_tipo.get()
        self.material = self.e_material.get()
        self.descricao = self.e_descricao.get()
    def add_fer(self):
        self.variavel()
        self.conecta_bd()
        lista = [self.part_number, self.fabricante, self.tamanho, self.medida, self.volts, self.tipo, self.material, self.descricao]
        if self.part_number == '':
            messagebox.showerror('Erro', "O campo PART NUMBER não pode ser vazio")
        elif self.fabricante == '':
            messagebox.showerror('Erro', "O campo FABRICANTE não pode ser vazio")
        elif self.tamanho == '':
            messagebox.showerror('Erro', "O campo TAMANHO não pode ser vazio")
        elif self.medida == '':
            messagebox.showerror('Erro', "O campo UNIDADE DE MEDIDA não pode ser vazio")
        elif self.volts == '':
            messagebox.showerror('Erro', "O campo VOLTAGEM DA FERRAMENTA não pode ser vazio")
        elif self.tipo == '':
            messagebox.showerror('Erro', "O campo TIPO DA FERRAMENTA não pode ser vazio")
        elif self.material == '':
            messagebox.showerror('Erro', "O campo MATERIAL DA FERRAMENTA não pode ser vazio")
        elif self.descricao == '':
            messagebox.showerror('Erro', "O campo DESCRIÇÃO não pode ser vazio")
        else:
            self.inserir_info(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    def inserir_info(self,lista):
        self.variavel()
        self.conecta_bd()
        self.cursor.execute("""INSERT INTO ferramentas (part_number, fabricante, tamanho, medida, volts, tipo, material, descricao)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",lista)
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("SELECT cod, part_number, fabricante, tamanho, medida, volts, tipo, material, descricao FROM ferramentas;")
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.variavel()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8,col9 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.e_part_number.insert(END, col2)
            self.e_fabricante.insert(END, col3)
            self.e_tamanho.insert(END, col4)
            self.e_medida.insert(END, col5)
            self.e_volts.insert(END, col6)
            self.e_tipo.insert(END, col7)
            self.e_material.insert(END, col8)
            self.e_descricao.insert(END, col9)

    def deleta_fer(self):
        self.variavel()
        self.conecta_bd()
        self.cursor.execute(f"DELETE FROM ferramentas WHERE cod={self.codigo}")
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_fer(self):
        self.variavel()
        self.conecta_bd()
        lista = [self.part_number, self.fabricante, self.tamanho, self.medida, self.volts, self.tipo,
                      self.material, self.descricao]
        if self.part_number == '':
            messagebox.showerror('Erro', "O campo PART NUMBER não pode ser vazio")
        elif self.fabricante == '':
            messagebox.showerror('Erro', "O campo FABRICANTE não pode ser vazio")
        elif self.tamanho == '':
            messagebox.showerror('Erro', "O campo TAMANHO não pode ser vazio")
        elif self.medida == '':
            messagebox.showerror('Erro', "O campo UNIDADE DE MEDIDA não pode ser vazio")
        elif self.volts == '':
            messagebox.showerror('Erro', "O campo VOLTAGEM DA FERRAMENTA não pode ser vazio")
        elif self.tipo == '':
            messagebox.showerror('Erro', "O campo TIPO DA FERRAMENTA não pode ser vazio")
        elif self.material == '':
            messagebox.showerror('Erro', "O campo MATERIAL DA FERRAMENTA não pode ser vazio")
        elif self.descricao == '':
            messagebox.showerror('Erro', "O campo DESCRIÇÃO não pode ser vazio")
        else:
            self.update(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    def update(self,lista):
        self.variavel()
        self.conecta_bd()
        self.cursor.execute("""UPDATE ferramentas SET part_number=?, fabricante=?, tamanho=?, medida=?, volts=?, tipo=?, material=?, descricao=? WHERE cod=?
        WHERE cod = ?""", lista)
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def busca_fer(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.e_fabricante.insert(END, '%')
        fabricante = self.e_fabricante.get()
        self.cursor.execute(
            """SELECT cod, part_number, fabricante, tamanho, medida, volts, tipo, material, descricao FROM ferramentas
            WHERE fabricante LIKE '%s' ORDER BY fabricante ASC""" % fabricante)

        busca_part_number = self.cursor.fetchall()
        for i in busca_part_number:
            self.listaCli.insert("", END,values=i)
        self.desconecta_bd()





############### CRIANDO JANELA ###############
class Application(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.janela = janela
        self.validaEntradaPart()
        self.validaEntradasTextos()
        self.validaEntradaCodigo()
        self.tela()
        self.frames_da_tela()
        self.lista_frame()
        self.limpa_tela()
        self.montaTabelas()
        self.select_lista()
        self.Menu()
        self.janela.mainloop()
    def tela(self):
        self.janela.title("CONSULTA E CADASTRO DE FERRAMENTAS")
        self.janela.geometry("1060x483")
        self.janela.iconbitmap("img/ferra.ico")
        self.janela.configure(background="#e9edf5")
        self.janela.resizable(width=False, height=False)
    def frames_da_tela(self):
        self.frame_cima = Frame(self.janela, width=310, height=50, background="#4fa882", relief='flat')
        self.frame_cima.grid(row=0,column=0)

        self.frame_baixo = Frame(self.janela, width=310, height=403, background="#feffff", relief='flat')
        self.frame_baixo.grid(row=1,column=0,padx=0, pady=1, sticky="NSWE")

        self.frame_direita = Frame(self.janela, width=760, height=450, background="#feffff", relief='flat')
        self.frame_direita.place(x=311, y=0)

        ############## Label Cima #################
        self.app_name = Label(self.frame_cima, text="Consulta/Cadastro de Ferrametas", anchor=NW, font="Ivi 13 bold", bg="#4fa882",
                         fg="#feffff", relief='flat')
        self.app_name.place(x=10, y=20)


        ############## Configurando Frame Baixo #################

        # part_number
        self.l_part_number = Label(self.frame_baixo, text="Part Number *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d", relief='flat')
        self.l_part_number.place(x=10, y=10)
        self.e_part_number = Entry(self.frame_baixo, width=15, justify='left', relief='solid',  validate="key", validatecommand=self.vccp)
        self.e_part_number.place(x=15, y=35)

        # fabricante
        self.l_fabricante = Label(self.frame_baixo, text="Fabricante *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                             relief='flat')
        self.l_fabricante.place(x=125, y=10)
        self.e_fabricante = Entry(self.frame_baixo, width=28, justify='left', relief='solid')
        self.e_fabricante.place(x=130, y=35)

        # tamanho
        self.l_tamanho = Label(self.frame_baixo, text="Tamanho *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d", relief='flat')
        self.l_tamanho.place(x=10, y=60)
        self.e_tamanho = Entry(self.frame_baixo, width=10, justify='left', relief='solid',  validate="key", validatecommand=self.vccd)
        self.e_tamanho.place(x=15, y=85)

        # medida
        self.l_medida = Label(self.frame_baixo, text="Uni. Medida *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                         relief='flat')
        self.l_medida.place(x=100, y=60)
        self.lista_medida = ["Centimetro", "Milimetro", "Polegada"]
        self.e_medida = Combobox(self.frame_baixo, width=10, values=self.lista_medida,  validate="key", validatecommand=self.vctx)
        self.e_medida.place(x=105, y=85)

        # volts
        self.l_volts = Label(self.frame_baixo, text="Voltagem *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d", relief='flat')
        self.l_volts.place(x=200, y=60)
        self.lista_volts = ["127v", "220v", "12v", "Nenhuma"]
        self.e_volts = Combobox(self.frame_baixo, width=10, values=self.lista_volts)
        self.e_volts.place(x=205, y=85)

        # tipo
        self.l_tipo = Label(self.frame_baixo, text="Tipo da Ferramenta *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                       relief='flat')
        self.l_tipo.place(x=10, y=110)
        self.e_tipo = Entry(self.frame_baixo, width=47, justify='left', relief='solid')
        self.e_tipo.place(x=15, y=135)

        # material
        self.l_material = Label(self.frame_baixo, text="Material da Ferramenta *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                           relief='flat')
        self.l_material.place(x=10, y=160)
        self.e_material = Entry(self.frame_baixo, width=47, justify='left', relief='solid')
        self.e_material.place(x=15, y=185)

        # descricao
        self.l_descricao = Label(self.frame_baixo, text="Descrição *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                            relief='flat')
        self.l_descricao.place(x=10, y=210)
        self.e_descricao = Entry(self.frame_baixo, width=47, justify='left', relief='solid')
        self.e_descricao.place(x=15, y=235)

        # CODIGO
        self.l_codigo = Label(self.frame_baixo, text="ID", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                              relief='flat')
        self.l_codigo.place(x=10, y=260)
        self.codigo_entry = Entry(self.frame_baixo, width=10, justify='left', relief='solid', validate="key",
                                  validatecommand=self.vccd)
        self.codigo_entry.place(x=15, y=285)

        # Botão inserir
        self.b_inserir = Button(self.frame_baixo, text="Inserir", width=10, font="Ivi 10 bold", bg="#4fa882", fg="#feffff", relief='raised',
                           overrelief='ridge', command=self.add_fer)
        self.b_inserir.place(x=15, y=320)

        # Botão atualizar
        self.b_atualizar = Button(self.frame_baixo, command=self.altera_fer, text="Atualizar", width=10, font="Ivi 10 bold", bg="#4fa882", fg="#feffff", relief='raised', overrelief='ridge')
        self.b_atualizar.place(x=110, y=320)

        # Botão deletar
        self.b_deletar = Button(self.frame_baixo, command=self.deleta_fer, text="Deletar", width=10, font="Ivi 10 bold", bg="#4fa882", fg="#feffff",
                           relief='raised', overrelief='ridge')
        self.b_deletar.place(x=205, y=320)

        # Botão limpar
        self.b_limpar = Button(self.frame_baixo, command=self.limpa_tela, text="Limpar", width=10,font="Ivi 10 bold", bg="#038cfc", fg="#feffff",relief='raised', overrelief='ridge')
        self.b_limpar.place(x=15,y=360)

        # Botão BuscarFabricante
        self.b_buscar = Button(self.frame_baixo, command=self.busca_fer, text="Buscar \ Fabric.", width=12, font="Ivi 10 bold",
                               bg="#4fa882", fg="#feffff", relief='raised', overrelief='ridge')
        self.b_buscar.place(x=111, y=360)

    def lista_frame(self):

        self.listaCli = ttk.Treeview(self.frame_direita, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9"))
        self.listaCli.heading("#1", text="ID")
        self.listaCli.heading("#2", text="P/N")
        self.listaCli.heading("#3", text="Fabricante")
        self.listaCli.heading("#4", text="Tamanho")
        self.listaCli.heading("#5", text="Medida")
        self.listaCli.heading("#6", text="Volts")
        self.listaCli.heading("#7", text="Tipo")
        self.listaCli.heading("#8", text="Material")
        self.listaCli.heading("#9", text="Descrição")

        self.listaCli.column("#0", width=0)
        self.listaCli.column("#1", width=5)
        self.listaCli.column("#2", width=15)
        self.listaCli.column("#3", width=50)
        self.listaCli.column("#4", width=15)
        self.listaCli.column("#5", width=15)
        self.listaCli.column("#6", width=15)
        self.listaCli.column("#7", width=70)
        self.listaCli.column("#8", width=70)
        self.listaCli.column("#9", width=70)

        self.listaCli.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.94)

        self.scroolListaV = Scrollbar(self.frame_direita, orient="vertical")
        self.listaCli.configure(yscrollcommand=self.scroolListaV)
        self.scroolListaV.place(x=730, y=5, height=426)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def Menu(self):
        menubar = Menu(self.janela)
        self.janela.configure(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatório", menu= filemenu2)
        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Gerar Relatório", command=self.geraRelatTec)
    def validaEntradaPart(self):
        self.vccp = (self.janela.register(self.validate_entryPart), "%P")
    def validaEntradasTextos(self):
        self.vctx = (self.janela.register(self.validate_Textos), "%P")
    def validaEntradaCodigo(self):
        self.vccd = (self.janela.register(self.validate_entryCodigo), "%P")



Application()