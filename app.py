# Importanto tkinter - biblioteca GUI
from tkinter import *
from tkinter import Tk, StringVar, ttk
from ttkthemes import ThemedStyle
from tktooltip import ToolTip
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# definindo paleta de cores
color1 = "#000000"  # preto
color2 = "#F0F8FF"  # branco
color3 = "#008000"  # verde
color4 = "#0000FF"  # azul
color5 = " "
color6 = " "
color7 = " "
color8 = " "


# Criando janela principal
home = Tk()
home.title("Solareli Energia Solar - Monitoramento")  # Titulo
home.geometry('900x600')  # Define um tamanho inicial
home.configure(bg=color1)  # Background
# Tema/Estilo da janela
style = ttk.Style(home)
style.theme_use("clam")

# Habilitando o redimensionamento da janela
home.resizable(True, True)
# Configurando o comportamento de redimensionamento dos frames
# Permite que framMid expanda verticalmente
home.grid_rowconfigure(1, weight=1)
# Permite que os frames expandam horizontalmente
home.grid_columnconfigure(1, weight=1)

# Obtendo a largura e altura da tela do monitor
largura_tela = home.winfo_screenwidth()
altura_tela = home.winfo_screenheight()

# Definindo a geometria para que a janela se ajuste à tela
home.geometry(f'{largura_tela}x{altura_tela}')


# Frames/Divs
frameSup = Frame(home, width=largura_tela, height=50, bg=color2, relief=FLAT)
frameSup.grid(row=0, column=0, sticky=NSEW)

frameMid = Frame(home, width=largura_tela, height=altura_tela -
                 100, bg=color2, pady=1, relief=FLAT)
frameMid.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameBott = Frame(home, width=largura_tela, height=300,
                  bg=color2, pady=1, relief=FLAT)
frameBott.grid(row=2, column=0, pady=0, padx=1, sticky=NSEW)

# frameSup:
# Adicionar Logo
app_img = Image.open('icondashboard.png')  # Carrega a imagem
app_img = app_img.resize((45, 45))  # Define o tamanho
app_img = ImageTk.PhotoImage(app_img)  # Transforma em foto

app_logo = Label(frameSup, image=app_img, text=' Solareli Energia Solar - Dashboard de Monitoramento', width=largura_tela,
                 compound=LEFT, relief=RAISED, anchor=CENTER, font=('Helvetica 20 bold'), bg=color2, fg=color1)
app_logo.place(x=0, y=0)  # Cria o objeto label

# Criando label para exibir a data e hora


def watch():
    # Coleta a hora atual e coloca no formato
    calendar = datetime.now().strftime("%d/%M/%Y - %H:%M:%S")
    l_calendar.config(text=calendar)  # Passa calendar como texto da label
    l_calendar.after(1000, watch)  # Delay de 1s.


l_calendar = Label(frameSup, text="", font=('Helvetica 12'),
                   bg=color2)  # Cria o objeto label
l_calendar.grid(padx=10, pady=10, sticky=E)
watch()  # Executa o relógio


# framMid:
# Lista clientes
def att_Clientes():
    conn = sql.connect("dados_geracao.db")  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria um apontador no BD
    # Executa a tabela com coluna desejada
    cursor.execute("SELECT id_cliente, cliente FROM clientes")
    clientes = cursor.fetchall()  # Captura os valores das colunas em tuplas
    conn.close()  # Fecha a conexão
    return clientes  # Retorna o valor das colunas


frame1 = Frame(frameMid, width=240, height=200,
               bg=color2, relief=RIDGE, borderwidth=2)
frame1.grid(row=0, column=0, padx=2, pady=0, sticky=NSEW)
frame1.grid_propagate(False)

frame2 = Frame(frameMid, width=300, height=350,
               bg=color2, relief=RIDGE, borderwidth=2)
frame2.grid(row=0, column=1, padx=2, pady=0, sticky=NSEW)

frame3 = Frame(frameMid, width=300, height=350,
               bg=color2, relief=RIDGE, borderwidth=2)
frame3.grid(row=0, column=2, padx=2, pady=0, sticky=NSEW)

frame4 = Frame(frameMid, width=500, height=395,
               bg=color2, relief=RIDGE, borderwidth=2)
frame4.grid(row=0, column=3, padx=2, pady=0, sticky=N)

l_cliente = Label(frame1, text="Clientes:", bg=color2)
l_cliente.grid(row=0, column=0, padx=1, pady=1, sticky=W)

selected_cliente = StringVar()  # Rastreia a seleção do combobox
clientes = att_Clientes()  # Guarda o retorno da função


# Lista que será exibida no combobox
clientes_exibicao = [""] + [
    f"{id_cliente} - {nome_cliente}" for id_cliente, nome_cliente in clientes]
# Criar o combobox
combobox_cliente = ttk.Combobox(
    frame1, textvariable=selected_cliente, values=clientes_exibicao, state="readonly", width=20)
combobox_cliente.grid(row=0, column=1, padx=2, pady=10, sticky=N)


# Cria a label de resposta ao selecionar o cliente
cliente_selecionado = Label(frame1, text="", font=('Helvetica 8'), bg=color2)
cliente_selecionado.grid(row=2, column=0, columnspan=3,
                         padx=2, pady=0, sticky=W)


def selecionar_cliente(event):
    selected_text = selected_cliente.get()
    split_text = selected_text.split(" - ", 1)
    if len(split_text) == 2:
        selected_id_cliente, selected_nome_cliente = split_text
        mensagem = f"Cliente localizado: {selected_id_cliente} \n {selected_nome_cliente}"
        cor = "blue"
        # Aqui você deve obter os valores para cada mês correspondente ao cliente
        # Suponhamos que 'valores' seja uma lista com os valores.
        valores = obter_valores_do_cliente(selected_id_cliente)
        # Chama a função para gerar o gráfico
        for widget in frame4.winfo_children():
            widget.destroy()

        gerar_grafico(selected_nome_cliente, valores)
    else:
        mensagem = "Cliente não localizado"
        cor = "red"
    cliente_selecionado.config(text=mensagem, fg=cor)


# Campo de busca
entrada_pesquisa = Entry(frame1, width=20)
entrada_pesquisa.grid(row=1, column=1, padx=2, pady=0, sticky=W)


def pesquisar_cliente():
    termo_pesquisa = entrada_pesquisa.get()
    resultados = [cliente for cliente in clientes_exibicao if termo_pesquisa.lower(
    ) in cliente.lower()]
    combobox_cliente['values'] = resultados

    if not resultados:
        cliente_selecionado.config(text="Cliente não localizado", fg="red")
    else:
        cliente_selecionado.config(
            text=f"{len(resultados)} clientes encontrados", fg="blue")


# Botão de Busca
botao_pesquisar = Button(frame1, text="Buscar", command=pesquisar_cliente)
botao_pesquisar.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)

# Associando a função ao evento de seleção no combobox
combobox_cliente.bind("<<ComboboxSelected>>", selecionar_cliente)


def obter_valores_do_cliente(id_cliente):
    conn = sql.connect("dados_geracao.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT janeiro, fevereiro, marco, abril, maio, junho, julho, agosto, setembro, outubro, novembro, dezembro FROM clientes WHERE id_cliente = {id_cliente}")
    # Assume-se que id_cliente é único, portanto, fetchone é suficiente
    valores = cursor.fetchone()
    conn.close()
    # Substituindo valores nulos por 0
    valores = [0 if valor is None else float(
        valor.replace(',', '.')) for valor in valores]

    return valores


# Gráficos
def gerar_grafico(cliente, valores):
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
             'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    # Remova os meses sem dados
    meses_com_dados = meses[:len(valores)]

    fig, ax = plt.subplots(figsize=(500/100, 390/100), dpi=100)
    bars = ax.bar(meses_com_dados, valores)

    plt.title('Geração Mensal (kWh/mês)')

    # Configurando o eixo y para começar em zero
    plt.ylim(0)

    # Adicionando os rótulos no topo das barras
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval,
                round(yval, 2), ha='center', va='bottom', fontsize=8)

    # fig.set_size_inches(5, 3)
    # plt.show()

    # Criando uma instância de FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas.draw()

    # Adicionando o canvas ao frame4
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=False)

    # Adicionando a barra de navegação
    # toolbar = NavigationToolbar2Tk(canvas, frame4)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=False)


home.mainloop()
