import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.io as pio

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    frames = []

    # Contar las ocurrencias en los "buckets"
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    # Modificar count para reflejar posiciones reales en output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Construir el arreglo de salida
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        # Guardar el estado para animación
        frames.append({
            'arr': output.copy(),
            'digit': exp,
            'current': i,
            'bucket': index % 10
        })

    # Copiar el arreglo de salida a arr[]
    for i in range(n):
        arr[i] = output[i]

    return frames

def radix_sort_with_animation(arr):
    max_num = max(arr)
    exp = 1
    frames = []

    # Aplicar counting sort para cada dígito
    while max_num // exp > 0:
        frames.extend(counting_sort(arr, exp))
        exp *= 10

    return frames

def create_animation(frames, output_file='radix_sort_animation.html'):
    fig = make_subplots(rows=1, cols=1)
    
    # Función para crear las barras en cada frame
    def create_bar_trace(arr, digit, current, bucket):
        colors = ['lightblue' for _ in range(len(arr))]
        if current is not None and current >= 0:
            colors[current] = 'red'
        text = [str(val) for val in arr]  # Texto con los valores
        return go.Bar(
            y=arr,
            marker_color=colors,
            text=text,
            textposition='outside',
            hoverinfo='text'
        )
    
    # Añadir el primer frame
    fig.add_trace(create_bar_trace(frames[0]['arr'], frames[0]['digit'], frames[0]['current'], frames[0]['bucket']))
    
    # Crear los frames para la animación
    fig_frames = [go.Frame(data=[create_bar_trace(frame['arr'], frame['digit'], frame['current'], frame['bucket'])],
                           name=str(idx)) 
                  for idx, frame in enumerate(frames)]
    
    fig.frames = fig_frames
    
    # Configuración de botones de animación
    fig.update_layout(
        title='Animación de Radix Sort',
        xaxis=dict(range=[-1, len(frames[0]['arr'])]),
        yaxis=dict(range=[0, max(max(frame['arr']) for frame in frames) * 1.1]),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        annotations=[
            dict(text="Azul: Elemento no procesado", x=0, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(text="Rojo: Elemento actual", x=1, y=1.05, xref="paper", yref="paper", showarrow=False)
        ]
    )
    
    # Exportar la animación a un archivo HTML sin auto reproducir
    pio.write_html(fig, file=output_file, auto_open=True, auto_play=False)
    print(f"La animación ha sido guardada en {output_file}")

# Ejemplo de uso
arr = np.random.randint(1, 1000, 20)
frames = radix_sort_with_animation(arr)
create_animation(frames)
