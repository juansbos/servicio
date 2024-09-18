import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.io as pio

def counting_sort_with_animation(arr):
    frames = []
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1

    # Inicializar el array de conteo
    count = [0] * range_val

    # Contar ocurrencias
    for num in arr:
        count[num - min_val] += 1
        frames.append({
            'stage': 'count',
            'arr': arr.copy(),
            'count': count.copy(),
            'output': [],
            'current': num
        })

    # Calcular las posiciones acumuladas
    cumulative_count = count.copy()
    for i in range(1, len(cumulative_count)):
        cumulative_count[i] += cumulative_count[i-1]
        frames.append({
            'stage': 'accumulate',
            'arr': arr.copy(),
            'count': count.copy(),
            'cumulative_count': cumulative_count.copy(),
            'output': [],
            'current': i + min_val
        })

    # Construir el array ordenado
    output = [0] * len(arr)
    for num in reversed(arr):
        index = cumulative_count[num - min_val] - 1
        output[index] = num
        cumulative_count[num - min_val] -= 1
        frames.append({
            'stage': 'place',
            'arr': arr.copy(),
            'count': count.copy(),
            'cumulative_count': cumulative_count.copy(),
            'output': output.copy(),
            'current': num
        })

    return frames

def create_animation(frames, output_file='counting_sort_animation.html'):
    fig = make_subplots(rows=3, cols=1, 
                        subplot_titles=("Array Original", "Conteo de Ocurrencias", "Array Ordenado"),
                        row_heights=[0.33, 0.33, 0.33],
                        vertical_spacing=0.1)

    max_val = max(max(frame['arr']) for frame in frames)
    min_val = min(min(frame['arr']) for frame in frames)
    max_count = max(max(frame['count']) for frame in frames)

    pastel_blue = 'rgb(173, 216, 230)'  # Light Blue
    pastel_green = 'rgb(152, 251, 152)'  # Pale Green
    pastel_orange = 'rgb(255, 229, 180)'  # Light Peach

    def create_bar_trace(arr, current=None, color=pastel_blue):
        colors = [color if x != current else 'rgb(255, 105, 97)' for x in arr]  # Light Coral for current
        return go.Bar(y=arr, marker_color=colors, text=[str(x) for x in arr], textposition='outside', hoverinfo='text')

    def create_count_trace(count, color=pastel_green):
        x_values = list(range(len(count)))
        x_labels = [str(i + min_val) for i in x_values]  # Etiquetas del eje x
        return go.Bar(
            x=x_labels, 
            y=count, 
            marker_color=color, 
            text=[str(x) for x in count],  # Mostrar el texto del conteo
            textposition='outside', 
            hoverinfo='text',
            name='Frecuencia'
        )

    # Crear el primer frame
    fig.add_trace(create_bar_trace(frames[0]['arr'], frames[0]['current']), row=1, col=1)
    fig.add_trace(create_count_trace(frames[0]['count']), row=2, col=1)
    fig.add_trace(create_bar_trace(frames[0]['output'], color=pastel_orange), row=3, col=1)

    # Crear los frames para la animación
    fig_frames = []
    for frame in frames:
        fig_frames.append(go.Frame(
            data=[
                create_bar_trace(frame['arr'], frame['current']),
                create_count_trace(frame['count']),
                create_bar_trace(frame['output'], frame['current'] if frame['stage'] == 'place' else None, pastel_orange)
            ],
            name=str(len(fig_frames))
        ))

    fig.frames = fig_frames

    # Configurar el diseño y los controles de animación
    fig.update_layout(
        title='Animación de Counting Sort',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])],
        )],
        height=900
    )

    fig.update_yaxes(range=[0, max_val * 1.1], row=1, col=1)
    fig.update_yaxes(range=[0, max_count * 1.1], row=2, col=1)
    fig.update_yaxes(range=[0, max_val * 1.1], row=3, col=1)

    # Exportar la figura a un archivo HTML sin auto_play
    pio.write_html(fig, file=output_file, auto_open=True, auto_play=False)
    print(f"La animación ha sido guardada en {output_file}")

# Generar un arreglo aleatorio
arr = np.random.randint(1, 20, 15)
frames = counting_sort_with_animation(arr)

# El botón "Play" controlará la animación
create_animation(frames)
