import tkinter as tk
from tkinter import font as tkfont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline

# Dados de vendas diárias de uma loja durante um mês (30 dias)
dados = {
    'Dia': range(1, 31),
    'Vendas': [
        150, 200, 250, 300, 100,
        400, 350, 300, 450, 200,
        250, 250, 300, 200, 100,
        400, 300, 350, 200, 250,
        200, 150, 400, 300, 250,
        350, 200, 150, 100, 300
    ]
}

# Convertendo os dados em um DataFrame do Pandas
df = pd.DataFrame(dados)

# Função para limpar widgets anteriores
def clear_frame():
    for widgets in window.winfo_children():
        if isinstance(widgets, tk.Canvas):
            widgets.destroy()

# Função para plotar as vendas diárias
def plot_vendas_diarias():
    clear_frame()
    fig = Figure(figsize=(12, 8))
    plot1 = fig.add_subplot(111)
    x_smooth = np.linspace(df['Dia'].min(), df['Dia'].max(), 300)
    spl = make_interp_spline(df['Dia'], df['Vendas'], k=3)
    y_smooth = spl(x_smooth)
    plot1.plot(x_smooth, y_smooth, linestyle='-', color='royalblue', linewidth=2, label='Vendas')
    plot1.scatter(df['Dia'], df['Vendas'], color='darkorange', label='Dados Diários')

    # Marcando o dia com venda máxima
    plot1.scatter(df['Dia'][df['Vendas'].idxmax()], df['Vendas'].max(), color='green', s=100, edgecolor='black', label='Venda Máxima')
    # Adicionando anotação para a venda máxima
    plot1.annotate('Máxima', xy=(df['Dia'][df['Vendas'].idxmax()], df['Vendas'].max()), xytext=(df['Dia'][df['Vendas'].idxmax()]+1, df['Vendas'].max()), arrowprops=dict(facecolor='black', shrink=0.05))

    # Marcando dias específicos com vendas mínimas
    dias_minimos = [5, 15, 29]  # Dias com vendas mínimas para marcar
    for dia in dias_minimos:
        venda_minima = df['Vendas'][dia - 1]  # -1 porque os índices do DataFrame começam em 0
        plot1.scatter(dia, venda_minima, color='red', s=100, edgecolor='black', label='Venda Mínima' if dia == dias_minimos[0] else "")
        # Ajustando a posição da anotação para a direita
        plot1.annotate('Mínima', xy=(dia, venda_minima), xytext=(dia + 0.5, venda_minima + 10), arrowprops=dict(facecolor='black', shrink=0.05))

    plot1.set_title('Vendas Diárias durante um Mês', fontsize=16)
    plot1.set_xlabel('Dia', fontsize=14, labelpad=15)
    plot1.set_ylabel('Vendas', fontsize=14, labelpad=15)
    
    # Configurando os ticks do eixo x para incluir todos os dias do mês
    plot1.set_xticks(df['Dia'])
    
    plot1.legend()
    plot1.grid(True, linestyle='--', alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()

# Função para plotar o gráfico de pizza das vendas por categoria
def plot_vendas_categoria():
    clear_frame()
    categorias = ['Eletrônicos', 'Vestuário', 'Alimentos', 'Farmácia']
    vendas_por_categoria = [500, 300, 400, 200]
    fig = Figure(figsize=(8, 8))
    plot2 = fig.add_subplot(111)
    plot2.pie(vendas_por_categoria, labels=categorias, autopct='%1.1f%%', startangle=140, colors=['blue', 'orange', 'green', 'red'])

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()
    
# Criando a janela principal do Tkinter
window = tk.Tk()
window.title("Visualização de Dados de Vendas")

# Ajustando o tamanho da janela
window_width = 1200
window_height = 900

# Obtendo as dimensões da tela
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculando a posição x e y para centralizar a janela, ajustando para ficar mais acima
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2 - 50)  # Ajuste aqui: subtraindo 50 para mover a janela para cima

# Configurando a geometria da janela com a nova posição
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Botões para alternar entre os gráficos
btn_frame = tk.Frame(window)
btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Definindo a fonte e o tamanho
customFont = tkfont.Font(family="Roboto", size=11)  # Ajuste o tamanho conforme necessário

btn_vendas_diarias = tk.Button(btn_frame, text="Vendas Diárias", command=plot_vendas_diarias, bg='#3CB371', width=20, height=2, font=customFont)
btn_vendas_diarias.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

btn_vendas_categoria = tk.Button(btn_frame, text="Vendas por Categoria", command=plot_vendas_categoria, bg='#3CB371', width=20, height=2, font=customFont)
btn_vendas_categoria.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

window.mainloop()
