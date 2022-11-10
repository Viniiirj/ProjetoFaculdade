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
    def validate_entryCPF(self, text):
        if text == "":
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <=99999999999
    def validate_entryCodigo(self, text):
        if text == "":
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <=999
    def validate_entryTelefone(self, text):
        if text == "":
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 99999999999
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
        self.e_nome.delete(0, END)
        self.e_cpf.delete(0, END)
        self.e_telefone.delete(0, END)
        self.e_equipe.delete(0, END)
        self.e_turno.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("cadastroTecnico.bd")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):
        self.conn.close()
    def montaTabelas(self):
        self.conecta_bd()
        print("Conectando ao banco de dados")
        # Criar tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tecnicos (
                                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                                tec_nome CHAR (40) NOT NULL,
                                cpf INTEGER(20) NOT NULL,
                                tel INTEGER(20)  NOT NULL,
                                nome_equipe CHAR(40) NOT NULL,
                                turno CHAR(20) NOT NULL
                                );""")
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()
    def variavel(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.e_nome.get()
        self.cpf = self.e_cpf.get()
        self.telefone = self.e_telefone.get()
        self.equipe = self.e_equipe.get()
        self.turno = self.e_turno.get()
    def add_tec(self):
        self.variavel()
        self.conecta_bd()
        lista = [self.nome, self.cpf, self.telefone, self.equipe, self.turno]
        if self.nome == '':
            messagebox.showerror('Erro', "O campo NOME não pode ser vazio")
        elif self.cpf == '':
            messagebox.showerror('Erro', "O campo CPF não pode ser vazio")
        elif self.telefone == '':
            messagebox.showerror('Erro', "O campo TAMANHO não pode ser vazio")
        elif self.equipe == '':
            messagebox.showerror('Erro', "O campo NOME DA EQUIPE não pode ser vazio")
        elif self.turno == '':
            messagebox.showerror('Erro', "O campo TURNO não pode ser vazio")
        else:
            self.inserir_info(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    def inserir_info(self,lista):
        self.variavel()
        self.conecta_bd()

        self.cursor.execute("""INSERT INTO tecnicos (tec_nome, cpf, tel, nome_equipe, turno) VALUES (?, ?, ?, ?, ?)""", lista)
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("SELECT cod, tec_nome, cpf, tel, nome_equipe, turno FROM tecnicos;")
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.e_nome.insert(END, col2)
            self.e_cpf.insert(END, col3)
            self.e_telefone.insert(END, col4)
            self.e_equipe.insert(END, col5)
            self.e_turno.insert(END, col6)
    def deleta_tec(self):
        self.variavel()
        self.conecta_bd()
        self.cursor.execute(f"DELETE FROM tecnicos WHERE cod={self.codigo}")
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_cliente(self):
        self.variavel()
        self.conecta_bd()
        lista = [self.nome, self.cpf, self.telefone, self.equipe, self.turno]
        if self.nome == '':
            messagebox.showerror('Erro', "O campo NOME não pode ser vazio")
        elif self.cpf == '':
            messagebox.showerror('Erro', "O campo CPF não pode ser vazio")
        elif self.telefone == '':
            messagebox.showerror('Erro', "O campo TAMANHO não pode ser vazio")
        elif self.equipe == '':
            messagebox.showerror('Erro', "O campo NOME DA EQUIPE não pode ser vazio")
        elif self.turno == '':
            messagebox.showerror('Erro', "O campo TURNO não pode ser vazio")
        else:
            self.update(lista)
            messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')
    def update(self,lista):
        self.variavel()
        self.conecta_bd()
        self.cursor.execute("""UPDATE tecnicos SET tec_nome=?, cpf=?, tel=?, nome_equipe=?, turno=?
        WHERE cod = ?""", (self.nome, self.cpf,self.telefone, self.equipe, self.turno, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def busca_tecnico(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.e_nome.insert(END, '%')
        nome = self.e_nome.get()
        self.cursor.execute(
            """SELECT cod, tec_nome, cpf, tel, nome_equipe, turno FROM tecnicos
            WHERE tec_nome LIKE '%s' ORDER BY tec_nome ASC""" % nome)

        buscanomeTec = self.cursor.fetchall()
        for i in buscanomeTec:
            self.listaCli.insert("", END,values=i)
        self.desconecta_bd()





############### CRIANDO JANELA ###############
class Application(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.janela = janela
        self.validaEntradaCPF()
        self.validaEntradasTextos()
        self.validaEntradaTelefone()
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
        self.janela.title("CONSULTA E CADASTRO DE TÉCNICOS")
        self.janela.geometry("940x480")
        self.janela.iconbitmap("tec.ico")
        self.janela.configure(background="#e9edf5")
        self.janela.resizable(width=False, height=False)
    def frames_da_tela(self):
        self.frame_cima = Frame(self.janela, width=310, height=50, background="#4fa882", relief='flat')
        self.frame_cima.grid(row=0,column=0)

        self.frame_baixo = Frame(self.janela, width=310, height=423, background="#feffff", relief='flat')
        self.frame_baixo.grid(row=1,column=0,padx=0, pady=1, sticky="NSWE")

        self.frame_direita = Frame(self.janela, width=588, height=423, background="#feffff", relief='flat')
        self.frame_direita.grid(row=0,column=1, rowspan=2, padx=1, pady=0, sticky="NSWE")

        ############## Label Cima #################
        self.app_name = Label(self.frame_cima, text="Consulta/Cadastro de Técnicos", anchor=NW, font="Ivi 13 bold", bg="#4fa882",
                         fg="#feffff", relief='flat')
        self.app_name.place(x=10, y=20)
        ############## Configurando Frame Baixo #################
        # Nome
        self.l_nome = Label(self.frame_baixo, text="Nome *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",relief='flat')
        self.l_nome.place(x=10,y=10)
        self.e_nome = Entry(self.frame_baixo, width=45, justify='left', relief='solid')
        self.e_nome.place(x=15,y=40)

        # CPF
        self.l_cpf = Label(self.frame_baixo, text="CPF *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",relief='flat')
        self.l_cpf.place(x=10,y=70)
        self.e_cpf = Entry(self.frame_baixo, width=45, justify='left', relief='solid',  validate="key", validatecommand=self.vccp)
        self.e_cpf.place(x=15,y=100)

        # Telefone
        self.l_telefone = Label(self.frame_baixo, text="Telefone *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",relief='flat')
        self.l_telefone.place(x=10,y=130)
        self.e_telefone = Entry(self.frame_baixo, width=45, justify='left', relief='solid',  validate="key", validatecommand=self.vctel)
        self.e_telefone.place(x=15,y=160)

        # Equipe
        self.l_equipe = Label(self.frame_baixo, text="Nome da Equipe *", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",relief='flat')
        self.l_equipe.place(x=10,y=190)
        self.e_equipe = Entry(self.frame_baixo, width=28, justify='left', relief='solid')
        self.e_equipe.place(x=15,y=220)

        # Turno
        self.l_turno = Label(self.frame_baixo, text="Turno *", anchor=NW, font="Ivi 10 bold", bg="#feffff",
                             fg="#403d3d", relief='flat')
        self.l_turno.place(x=200, y=190)
        self.lista_turnos = ["Manhã", "Tarde", "Noite"]
        self.e_turno = Combobox(self.frame_baixo, width=10, values=self.lista_turnos)
        self.e_turno.place(x=205, y=220)

        #CODIGO
        self.l_codigo = Label(self.frame_baixo, text="ID", anchor=NW, font="Ivi 10 bold", bg="#feffff", fg="#403d3d",
                            relief='flat')
        self.l_codigo.place(x=10, y=250)
        self.codigo_entry = Entry(self.frame_baixo, width=10, justify='left', relief='solid', validate="key", validatecommand=self.vccd)
        self.codigo_entry.place(x=15, y=280)

        # Botão limpar
        self.b_limpar = Button(self.frame_baixo, command=self.limpa_tela, text="Limpar", width=10,font="Ivi 10 bold", bg="#038cfc", fg="#feffff",relief='raised', overrelief='ridge')
        self.b_limpar.place(x=15,y=360)

        # Botão BuscarNome
        self.b_buscar = Button(self.frame_baixo, command=self.busca_tecnico, text="Buscar \ Nome", width=12, font="Ivi 10 bold",
                               bg="#4fa882", fg="#feffff", relief='raised', overrelief='ridge')
        self.b_buscar.place(x=111, y=360)

        # Botão inserir
        self.b_inserir = Button(self.frame_baixo,command=self.add_tec, text="Inserir", width=10,font="Ivi 10 bold", bg="#038cfc", fg="#feffff",relief='raised', overrelief='ridge')
        self.b_inserir.place(x=15,y=320)

        # Botão atualizar
        self.b_atualizar = Button(self.frame_baixo, text="Atualizar", width=10,font="Ivi 10 bold", bg="#4fa882", fg="#feffff",relief='raised', overrelief='ridge', command=self.altera_cliente)
        self.b_atualizar.place(x=110,y=320)

        # Botão deletar
        self.b_deletar = Button(self.frame_baixo, text="Deletar", width=10,font="Ivi 10 bold", bg="#ef5350", fg="#feffff",relief='raised', overrelief='ridge', command=self.deleta_tec)
        self.b_deletar.place(x=205,y=320)
    def lista_frame(self):

        self.listaCli = ttk.Treeview(self.frame_direita, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaCli.heading("#1", text="ID")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="CPF")
        self.listaCli.heading("#4", text="Telefone")
        self.listaCli.heading("#5", text="Nome da Equipe")
        self.listaCli.heading("#6", text="Turno")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=5)
        self.listaCli.column("#2", width=150)
        self.listaCli.column("#3", width=90)
        self.listaCli.column("#4", width=90)
        self.listaCli.column("#5", width=100)
        self.listaCli.column("#6", width=70)

        self.listaCli.place(relx=0.01, rely=0.01, relwidth=0.96, relheight=0.94)

        self.scroolListaV = Scrollbar(self.frame_direita, orient="vertical")
        self.listaCli.configure(yscrollcommand=self.scroolListaV)
        self.scroolListaV.place(x=570, y=5, height=446)
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
    def validaEntradaCPF(self):
        self.vccp = (self.janela.register(self.validate_entryCPF), "%P")
    def validaEntradasTextos(self):
        self.vctx = (self.janela.register(self.validate_Textos), "%P")
    def validaEntradaTelefone(self):
        self.vctel = (self.janela.register(self.validate_entryTelefone), "%P")
    def validaEntradaCodigo(self):
        self.vccd = (self.janela.register(self.validate_entryCodigo), "%P")



Application()
