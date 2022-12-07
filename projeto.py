#importação das bibliotecas
from tkinter import *
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PCM(Toplevel):

    def __init__(self, original):
        #inicialização do frame da tela
        self.frame_original = original
        Toplevel.__init__(self)
        self.resizable(False, False)
        # definindo tamanho de janela
        self.largura = 1000
        self.altura = 700
        self.largura_screen = self.winfo_screenwidth()
        self.altura_screen = self.winfo_screenheight()
        self.posx = self.largura_screen/2 - self.largura/2
        self.posy = self.altura_screen/2 - self.altura/2
        self.geometry("%dx%d+%d+%d" % (self.largura, self.altura, self.posx, self.posy))
        self.title("Resultados")
        self.iconbitmap("icon.ico")
        self['bg'] = 'white'
        #criando a variavel responsavel por guardar a frequencia da onda 
        self.frenquencia = StringVar()
        # Criando as repartições da paginas
        self.rows = 0
        while self.rows < 50:
            self.rowconfigure(self.rows, weight=1)
            self.columnconfigure(self.rows, weight=1)
            self.rows += 1
        self.nb = ttk.Notebook(self)
        self.nb.grid(row=0, column=0, columnspan=50, rowspan=49, sticky='NEWS')
        self.page1 = ttk.Frame(self.nb)
        self.nb.add(self.page1, text="Iniciando a Onda")
        self.page2 = ttk.Frame(self.nb)
        self.nb.add(self.page2, text="Onda Amostrada")
        self.page3 = ttk.Frame(self.nb)
        self.nb.add(self.page3, text="Onda Quantizada")
        self.page4 = ttk.Frame(self.nb)
        self.nb.add(self.page4, text="Onda Codificada")
    # Criando os elementos da pagina 1
        self.labelI1 = Label(
            self.page1,
            text='Para começar vamos criar uma onda senoidal, para aplicar o PCM', 
            fg='black',
            font="Verdana 15 bold",
            justify=CENTER,
            padx=20).grid(row=1, columnspan=3, pady= 12, padx= 100)
        self.labelI2 = Label(
            self.page1,
            text='Entre com uma Frequência para a onda: ',
            fg='black',
            font="Verdana 14",
            justify='right').grid(row=2, padx=120)
        self.textboxI1 = Entry(
            self.page1, 
            textvariable=self.frenquencia,
            justify=CENTER).grid(row=2, column=1, pady= 12)
        self.btnO = Button(
            self.page1,
            text='Ver a Onda',
            font="Verdana 10",
            width= 15,
            height=2,
            command= lambda: self.ondaSenoidal()).grid(row=4, columnspan=3, pady= 10)
        self.btn = Button(
            self,
            text=' <- Voltar para o Inicio',
            command=self.onClose).grid()
        # Criando os elementos da pagina 2
        self.labelA = Label(
            self.page2,
            text='Amostragem da Onda',
            justify=CENTER,
            fg='black',
            font="Verdana 15 bold").grid(row=1, column=0, pady= 12, padx= 20)
        self.labelAdesc = Label(
            self.page2, 
            text='Nesta primeira etapa é feita a amostragem da onda através do método ideal, esta é uma das partes mais importantes para o PCM, pois é com ela que é possível identificar os pontos de amplitude da onda e assim traçar o seu caminho.',
            font="Verdana 12 ",
            fg='black',
            wraplength=self.largura - 50).grid(row=2, column=0, pady=12, padx=20)
        self.btnA = Button(
            self.page2,
            text= 'Ver Onda Amostrada',
            font="Verdana 10",
            width= 22,
            height=2,
            command= lambda: self.ondaAmostrada()).grid(row=4, pady=12)  
        # Criando os elementos da pagina 3
        self.labelQ = Label(
            self.page3,
            text='Quantização da Onda',
            justify=CENTER,
            fg='black',
            font='Verdana 15 bold').grid(row=1, column=0, columnspan=25, pady= 12,  padx= 40)
        self.labelQdesc = Label(
            self.page3,
            text=  'Após a onda está amostrada, os sinais mudaram de valor apenas em instantes discretos de tempo, mas assumiram valores em uma faixa contínua.' +
            'De modo que eles possam ser representados em um computador digital, assim também é necessário discretizar o sinal da amplitude. O arredondamento' +
            'dos valores na quantização pode ser um problema, caso esse arrendondamento seja muito grande por se causar o erro de quantização (ou ruído de quantização),' +
            'fazendo com que os dados analógicos gerados posteriormente fiquem diferentes dos dados analógicos originais.',
            justify=CENTER,
            fg='black',
            font='Verdana 12',
            wraplength=self.largura - 50).grid(row=2, column=0, columnspan=25, pady= 12, padx= 40)
        self.btnQ = Button(
            self.page3,
            text= 'Ver Onda Quantificada',
            font="Verdana 10",
            width= 22,
            height=2,
            command= lambda: self.ondaQuantizacao()).grid(row=5, columnspan=25)   
        # Criando os elementos da pagina 4
        self.labelC = Label(
            self.page4,
            text='Codificação da Onda',
            justify=CENTER,
            fg='black',
            font='Verdana 15 bold').grid(row=1, column=0, columnspan=100, pady=12)
        self.labelCdesc = Label(
            self.page4,
            text='Última etapa do processo PCM é a codificação, em que, após cada amostra ter sido quantizada e o número de bits por amostra ser decidido, cada amostra pode ser modificada para uma palavra de código de 𝑛𝑏 bits',
            justify=CENTER,
            fg='black',
            font='Verdana 12',
            wraplength=self.largura - 50).grid(row=2, column=0, columnspan=100, pady=12)
        self.btnQ = Button(
            self.page4,
            text= 'Ver Onda Quadrada',
            font="Verdana 10",
            width= 22,
            height=2,
            command= lambda: self.ondaQuadrada()).grid(row=5, columnspan=100, pady= 25)   
    # inicializando valores da onda
    def iniciaValor(self):
        self.t = np.linspace(0, 1, 25, endpoint=True)
        self.s = int(self.frenquencia.get()) + np.sin(self.t * int(self.frenquencia.get()))

    def ondaSenoidal(self):
        self.iniciaValor()

        #plotagem da onda atraves de um grafico
        figura = plt.Figure(figsize=(8, 4), dpi=100)
        ax = figura.add_subplot(111)
        ax.plot(self.t, self.s)
        ax.set(xlabel='Tempo', ylabel='Amplitude',
                title='Onda Senoidal')
        ax.grid(False)
        canvas = FigureCanvasTkAgg(figura, self.page1)
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, padx= 100)

    def ondaAmostrada(self):
        self.iniciaValor()

        #plotagem da onda atraves de um grafico
        figura = plt.Figure(figsize=(8, 4), dpi=100)
        ax = figura.add_subplot(111)
        ax.stem(self.t, self.s)
        ax.set(xlabel='Tempo', ylabel='Amplitude',
               title='Onda Amostrada')
        ax.grid(False)
        canvas = FigureCanvasTkAgg(figura, self.page2)
        canvas.get_tk_widget().grid(row=3, column=0)
        
    def ondaQuantizacao(self):
        self.iniciaValor()

        #realizando a quantização do sinal
        self.result = [[], []]
        for i, obj in enumerate(self.s):
            self.result[0].append(i+1)
            self.result[1].append(round(obj))

        #demostrando o resultado da quantização
        self.t_rows = len(self.result)
        self.t_col = len(self.result[0])
        for i in range(self.t_rows):
            for j in range(self.t_col):
                self.e = Entry(self.page3, 
                                width=3, fg='black',
                                font=('Arial',10,'bold'))
                self.e.grid(row=i+3, column=j)
                self.e.insert(END, self.result[i][j])

    def ondaQuadrada(self):
        self.iniciaValor()

        #codificação da onda
        self.listaCod = list()
        for i in range(len(self.s)):
            cobBinTrat = []
            codBin = f'{int(self.s[i]):b}'
            cobBinTrat = " ".join(codBin).split(" ")
            for b in range(len(cobBinTrat)):
                self.listaCod.append(int(cobBinTrat[b]))

        #exibindo a codificação da onda
        for i in range(len(self.listaCod)):
            self.cod = Entry(self.page4, width=1)
            self.cod.grid(row=3,column=i, pady=10)
            self.cod.insert(END, self.listaCod[i])

        #plotagem da onda atraves de um grafico
        figura = plt.Figure(figsize=(8, 4), dpi=100)
        ax = figura.add_subplot(111)
        ax.plot(self.listaCod) 
        ax.set(xlabel='Tempo', ylabel='Amplitude',
               title='Sinal Digital')
        ax.grid(False)
        canvas = FigureCanvasTkAgg(figura, self.page4)
        canvas.get_tk_widget().grid(row=4,columnspan=100)

    def onClose(self):
        self.destroy()
        self.frame_original.show()

class App:
    cor_btn = '#F8F8FF'

    #inicializando o Frame principal
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.tela_frame1()
        root.mainloop()

    def tela(self):
        self.root.title("PCM (Pulse Code Modulation)")
        self.root.resizable(False, False)
        # definindo o tamanho da tela
        self.largura = 1000
        self.altura = 700
        self.largura_screen = root.winfo_screenwidth()
        self.altura_screen = root.winfo_screenheight()
        self.posx = self.largura_screen/2 - self.largura/2
        self.posy = self.altura_screen/2 - self.altura/2
        self.root.geometry("%dx%d+%d+%d" % (self.largura, self.altura, self.posx, self.posy))
        self.root.iconbitmap("icon.ico")
        self.root['bg'] = 'white'

    def frames(self):
        self.frame1 = Frame(self.root, background='white')
        self.frame1.place(
            relx=0.09,
            rely=0.09,
            relwidth=0.90,
            relheight=0.90)

    def tela_frame1(self):
        self.label = Label(self.frame1,
                           text="PCM (Pulse Code Modulation)",
                           bg="white",
                           fg="black",
                           font="Verdana 20 bold",
                           width=40,
                           pady=40,
                           justify=CENTER).grid()
        self.label2 = Label(self.frame1,
                            text="Uma técnica de codificação que converte sinais analógicos em dados digitais",
                            bg="white",
                            fg="black",
                            font="Verdana 14 bold",
                            pady=10,
                            justify=CENTER).grid()
        self.label3 = Label(self.frame1,
                            text="PCM é composto por três processos:",
                            bg="white",
                            fg="black",
                            font="Verdana 13 bold",
                            width=60,
                            pady=10,
                            justify=CENTER).grid()

        self.imagem = PhotoImage(file='pcm.png')
       
        self.img1 = Label(
            self.frame1,
            image=self.imagem,
            bd=0,
            background= 'white').grid()

        self.btn_entrar = Button(
            self.frame1,
            text='Avançar',
            bg=self.cor_btn,
            font=('Verdana', 20),
            fg='black',
            border= 4,
            command=self.clica_entrar).grid(pady=50)

    def clica_entrar(self):
        self.hide()
        self.subFrame = PCM(self)

    def hide(self):  # Esconde a root
        self.root.withdraw()

    def show(self):  # Mostra a outra janela
        self.root.update()
        self.root.deiconify()

root = Tk()
App()
