from flask import Blueprint, render_template, request
from .controllers import get_optimal_route

# Crear un Blueprint para las rutas principales de la aplicación
main = Blueprint('main', __name__)

# Ruta principal que maneja las solicitudes GET y POST
@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        weight = request.form['weight']
        # Obtener la ruta óptima utilizando el controlador
        recommended_route, all_routes = get_optimal_route(origin, destination, weight)
        # Renderizar la plantilla de resultados con las rutas encontradas
        return render_template('result.html', recommended_route=recommended_route, all_routes=all_routes, weight=weight)
    # Renderizar la plantilla del formulario principal
    return render_template('index.html')
