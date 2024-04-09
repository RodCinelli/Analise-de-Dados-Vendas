from dash import Dash
import layouts

app = Dash(__name__)

app.layout = layouts.create_layout()

if __name__ == '__main__':
    app.run_server(debug=True)