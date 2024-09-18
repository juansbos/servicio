import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

def bucket_sort_with_animation(arr, num_buckets=5):
    frames = []
    n = len(arr)
    min_val, max_val = np.min(arr), np.max(arr)
    buckets = [[] for _ in range(num_buckets)]
    
    # Agregar el estado inicial aleatorio
    frames.append({
        'arr': arr.copy(),
        'buckets': [[] for _ in range(num_buckets)],
        'stage': 'initial',
        'current': -1
    })
    
    for i, num in enumerate(arr):
        normalized = (num - min_val) / (max_val - min_val)
        index = min(int(normalized * num_buckets), num_buckets - 1)
        buckets[index].append(num)
        frames.append({
            'arr': arr.copy(),
            'buckets': [bucket.copy() for bucket in buckets],
            'stage': 'distribute',
            'current': i
        })
    sorted_arr = []
    for i, bucket in enumerate(buckets):
        bucket.sort()
        sorted_arr.extend(bucket)
        frames.append({
            'arr': np.array(sorted_arr + [0] * (n - len(sorted_arr))),
            'buckets': [bucket.copy() for bucket in buckets],
            'stage': 'combine',
            'current': len(sorted_arr) - 1
        })
    return frames

def create_animation(frames, output_file='bucket_sort_animation.html'):
    fig = go.Figure()

    max_val = max(np.max(frame['arr']) for frame in frames)
    color_map = {
        'default': 'rgb(173, 216, 230)', 
        'active': 'rgb(255, 182, 193)', 
    }

    def create_array_trace(frame):
        colors = [color_map['default'] for _ in frame['arr']]
        if frame['stage'] in ['distribute', 'combine']:
            colors[frame['current']] = color_map['active']
        return go.Bar(
            y=frame['arr'],
            marker_color=colors,
            text=[str(x) for x in frame['arr']],
            textposition='outside',
            hoverinfo='text'
        )

    def create_buckets_text(frame):
        buckets_text = ""
        for i, bucket in enumerate(frame['buckets']):
            buckets_text += f"Bucket {i+1}: {', '.join(map(str, bucket)) if bucket else 'Vacío'}<br>"
        return f"<b>Estado de los buckets:</b><br>{buckets_text}"

    # Agregar el trace inicial (estado aleatorio)
    fig.add_trace(create_array_trace(frames[0]))

    # Crear los frames para la animación
    fig_frames = []
    for i, frame in enumerate(frames):
        frame_data = [create_array_trace(frame)]
        frame_layout = go.Layout(
            annotations=[
                dict(
                    text=create_buckets_text(frame),
                    xref="paper", yref="paper",
                    x=0.5, y=-0.4,
                    showarrow=False,
                    font=dict(size=14, color="black"),
                    align="center",
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor="rgba(0, 0, 0, 0.5)",
                    borderwidth=2,
                    opacity=0.9
                )
            ]
        )
        fig_frames.append(go.Frame(data=frame_data, layout=frame_layout, name=str(i)))

    fig.frames = fig_frames

    # Configurar el layout y los controles de la animación
    fig.update_layout(
        title='Bucket Sort Animation',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=500, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        height=700,
        margin=dict(l=20, r=20, t=100, b=200)
    )

    # Agregar la anotación inicial
    fig.add_annotation(
        text=create_buckets_text(frames[0]),
        xref="paper", yref="paper",
        x=0.5, y=-0.4,
        showarrow=False,
        font=dict(size=14, color="black"),
        align="center",
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="rgba(0, 0, 0, 0.5)",
        borderwidth=2,
        opacity=0.9
    )

    fig.update_yaxes(range=[0, max_val * 1.1])

    pio.write_html(fig, file=output_file, auto_open=True, auto_play=False)
    print(f"La animación ha sido guardada en {output_file}")

# Generar un arreglo aleatorio
arr = np.random.randint(1, 100, 9)
frames = bucket_sort_with_animation(arr, num_buckets=5)
create_animation(frames)