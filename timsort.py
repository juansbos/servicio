import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.io as pio

def insertion_sort(arr, left, right):
    frames = []
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            frames.append({
                'arr': arr.copy(),
                'stage': 'insertion',
                'active': list(range(left, right + 1)),
                'current': j + 1
            })
        arr[j + 1] = key
        frames.append({
            'arr': arr.copy(),
            'stage': 'insertion',
            'active': list(range(left, right + 1)),
            'current': j + 1
        })
    return frames

def merge(arr, left, mid, right):
    frames = []
    left_arr = arr[left:mid+1].copy()
    right_arr = arr[mid+1:right+1].copy()
    i = j = 0
    k = left

    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
        frames.append({
            'arr': arr.copy(),
            'stage': 'merge',
            'active': list(range(left, right + 1)),
            'current': k - 1
        })

    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
        frames.append({
            'arr': arr.copy(),
            'stage': 'merge',
            'active': list(range(left, right + 1)),
            'current': k - 1
        })

    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1
        frames.append({
            'arr': arr.copy(),
            'stage': 'merge',
            'active': list(range(left, right + 1)),
            'current': k - 1
        })

    return frames

def tim_sort_with_animation(arr):
    min_run = 32
    n = len(arr)
    frames = []

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        frames.extend(insertion_sort(arr, start, end))

    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            mid = start + size - 1
            end = min(start + size * 2 - 1, n - 1)
            if mid < end:
                frames.extend(merge(arr, start, mid, end))
        size *= 2

    return frames

def create_animation(frames, output_file='tim_sort_animation.html'):
    fig = make_subplots(rows=1, cols=1, subplot_titles=("Tim Sort"))

    max_val = max(max(frame['arr']) for frame in frames)

    color_map = {
        'default': 'rgb(0, 102, 204)',    # Strong Blue
        'active': 'rgb(0, 204, 102)',     # Strong Green
        'current': 'rgb(255, 105, 180)',  # Hot Pink
        'merged': 'rgb(255, 165, 0)'      # Orange
    }

    def create_bar_trace(frame):
        colors = [color_map['default'] for _ in frame['arr']]
        for i in frame['active']:
            colors[i] = color_map['active']
        if frame['stage'] == 'merge':
            for i in frame['active']:
                colors[i] = color_map['merged']
        if 'current' in frame:
            colors[frame['current']] = color_map['current']
        
        return go.Bar(
            y=frame['arr'],
            marker_color=colors,
            text=[str(x) for x in frame['arr']],
            textposition='outside',
            hoverinfo='text'
        )

    # Crear el primer frame
    fig.add_trace(create_bar_trace(frames[0]))

    # Crear los frames para la animación
    fig_frames = [go.Frame(data=[create_bar_trace(frame)], name=str(i)) 
                  for i, frame in enumerate(frames)]

    fig.frames = fig_frames

    # Configurar el diseño y los controles de animación
    fig.update_layout(
        title='Animación de Tim Sort',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=30, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        height=600
    )

    fig.update_yaxes(range=[0, max_val * 1.1])

    # Exportar la figura a un archivo HTML
    pio.write_html(fig, file=output_file, auto_open=True)
    print(f"La animación ha sido guardada en {output_file}")

# Ejemplo de uso
arr = np.random.randint(1, 100, 64)
frames = tim_sort_with_animation(arr)
create_animation(frames)
