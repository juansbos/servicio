import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.io as pio

def shell_sort_with_animation(arr):
    n = len(arr)
    gap = n // 2
    frames = []
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                frames.append({
                    'arr': arr.copy(),
                    'gap': gap,
                    'comparing': [j, j - gap],
                    'swapping': []
                })
            arr[j] = temp
            # Mostrar el estado después de la inserción
            frames.append({
                'arr': arr.copy(),
                'gap': gap,
                'comparing': [],
                'swapping': [j, i]  # Resaltar el intercambio final
            })
        gap //= 2
    
    return frames

def create_animation(frames, output_file='shell_sort_animation.html'):
    fig = make_subplots(rows=1, cols=1)
    
    def create_bar_trace(arr, comparing=None, swapping=None):
        colors = ['lightblue' for _ in range(len(arr))]
        if swapping:
            for idx in swapping:
                colors[idx] = 'lightpink'  # Rosa pastel para intercambio
        elif comparing:
            for idx in comparing:
                colors[idx] = 'red'  # Rojo para comparación
        return go.Bar(
            y=arr,
            marker_color=colors,
            text=arr,
            textposition='outside',
            hoverinfo='text'
        )
    
    # Crear el primer frame
    fig.add_trace(create_bar_trace(frames[0]['arr']))
    
    # Crear los frames para la animación
    fig_frames = [go.Frame(data=[create_bar_trace(frame['arr'], frame['comparing'], frame['swapping'])],
                           name=str(idx)) 
                  for idx, frame in enumerate(frames)]
    
    fig.frames = fig_frames
    
    # Configurar el diseño y los controles de animación
    fig.update_layout(
        title='Animación de Shell Sort',
        xaxis=dict(range=[-1, len(frames[0]['arr'])]),
        yaxis=dict(range=[0, max(frames[0]['arr']) * 1.1]),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=200, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        annotations=[
            dict(text="Rojo: Comparación", x=0, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(text="Rosa pastel: Intercambio", x=1, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(text="Paso: {frame_number}", x=0.5, y=-0.1, xref="paper", yref="paper", showarrow=False, 
                 font=dict(size=12, color="black"), align='center')
        ]
    )
    
    # Añadir anotaciones dinámicas de paso
    fig.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=200, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        annotations=[
            dict(text="Rojo: Comparación", x=0, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(text="Rosa pastel: Intercambio", x=1, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(
                text="Paso: {frame_number}", x=0.5, y=-0.1, xref="paper", yref="paper", showarrow=False, 
                font=dict(size=12, color="black"), align='center', name='step_annotation'
            )
        ]
    )

    # Actualizar la anotación del paso actual durante la animación
    fig.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=200, redraw=True),
                                           fromcurrent=True,
                                           mode='immediate')])]
        )],
        annotations=[
            dict(text="Rojo: Comparación", x=0, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(text="Rosa pastel: Intercambio", x=1, y=1.05, xref="paper", yref="paper", showarrow=False),
            dict(
                text="Paso: {frame_number}", x=0.5, y=-0.1, xref="paper", yref="paper", showarrow=False, 
                font=dict(size=12, color="black"), align='center', name='step_annotation'
            )
        ]
    )

    # Exportar la figura a un archivo HTML
    pio.write_html(fig, file=output_file, auto_open=True)
    print(f"La animación ha sido guardada en {output_file}")

# Ejemplo de uso
arr = np.random.randint(1, 100, 20)
frames = shell_sort_with_animation(arr)
create_animation(frames)
