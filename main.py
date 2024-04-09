from dash import Dash
import layouts

app = Dash(__name__)

app.layout = layouts.create_layout()

# Definindo o título do aplicativo
app.title = 'Análise de Vendas'

if __name__ == '__main__':
    app.run_server(debug=True)