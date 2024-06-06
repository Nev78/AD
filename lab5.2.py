#Імпортуємо бібліотеки
import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import dash_daq as daq
from scipy.signal import butter, filtfilt
# Ініціалізуємо додаток Dash
app = dash.Dash(__name__)

# Зберігаємо попередній шумовий сигнал
previous_noise_signal = None

def harmonic_with_noise(
    amplitude, frequency, phase, noise_mean, noise_covariance, show_noise=True, update_noise=True, 
):
    global previous_noise_signal
    t = np.linspace(0, 5, 1000)
    # Створюємо гармонійний сигнал
    harmonic_signal = amplitude * np.sin(2 * frequency * t + phase)

    if show_noise:
        if previous_noise_signal is None or update_noise:
            noise = np.random.multivariate_normal(
                [0, 0], [[noise_covariance, 0], [0, noise_covariance]], len(t)
            )
            noise_signal = noise[:, 0] + noise_mean
            previous_noise_signal = noise_signal
        else:
            noise_signal = previous_noise_signal
        signal = harmonic_signal + noise_signal

    else:
        signal = harmonic_signal

    return t, signal


def filter_signal(signal_to_filter, cutoff, fs):
    nyq = 0.5 *fs
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(2, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, signal_to_filter)
    return y


app.layout = html.Div([
    dcc.Graph(id='harmonic-graph'),
    html.Div([
        # Створення віджетів слайдерів
        html.Label('Amplitude'),
        # dcc.Input(id='amplitude-input', type='number', value=1),
        dcc.Slider(id="amplitude-input", min=0, max=5, value=1,),
        html.Label('Frequency'),
        dcc.Slider(id="frequency-input", min=0, max=10, value=3,),
        html.Label('Phase'),
        dcc.Slider( id="phase-input", min=0, max=2*3.14, value=0,),
        html.Label('Noise Mean'),
        dcc.Slider(id='noise-mean-input', min=-1, max=1, value=0),
        html.Label('Noise Covariance'),
        dcc.Slider(id='noise-covariance-input', min=0, max=0.2, value=0.01),
        html.Label('Filter Cutoff'),
        dcc.Slider(id='filter-cutoff', min=0, max=5, value=0.5),
        html.Label('Filter FS'),
        dcc.Slider(id='filter-fs', min=0, max=100, value=30),
    ], style={'width': '48%', 'float': 'left'}),
    
    html.Div([
        html.Div([
            #Створення кнопок і перемикачів
            html.Button('Reset', id='reset-button', n_clicks=0)
        ], style={'display': 'inline-block', 'width': '150px', 'text-align': 'right', 'margin-bottom': '10px', 'margin-top': '10px'}),
        html.Div([
            html.Label('Show Noise', style={'display': 'inline-block', 'width': '150px', 'text-align': 'right'}),
            daq.BooleanSwitch(id='show-noise-switch', on=True, style={'display': 'inline-block'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Show Filtered Signal', style={'display': 'inline-block', 'width': '150px', 'text-align': 'right'}),
            daq.BooleanSwitch(id='show-filter-switch', on=True, style={'display': 'inline-block'}),
        ], style={'margin-bottom': '10px'}),
    ])
])


@app.callback(
    Output('harmonic-graph', 'figure'),
    [
        Input('amplitude-input', 'value'),
        Input('frequency-input', 'value'),
        Input('phase-input', 'value'),
        Input('noise-mean-input', 'value'),
        Input('noise-covariance-input', 'value'),
        Input('show-noise-switch', 'on'),
        Input('show-filter-switch', 'on'),
        Input('filter-cutoff', 'value'),
        Input('filter-fs', 'value'),
        Input('reset-button', 'n_clicks')
    ]
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, show_filted_signal, filter_cutoff, filter_fs, n_clicks):
    # print(ctx.triggered_id)
    if (
        ctx.triggered_id == "noise-mean-input" or 
        ctx.triggered_id == "noise-covariance-input" or 
        ctx.triggered_id == "reset-button"
    ):
        update_noise = True

    else:
        update_noise = False
    t, signal = harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, update_noise)

    if show_filted_signal:
        filtered_signal = filter_signal(signal, cutoff=filter_cutoff, fs=filter_fs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=signal, mode='lines', name='Signal', showlegend=True))
    if show_filted_signal:
        fig.add_trace(go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal', showlegend=True))
    fig.update_layout(title='Noised Harmonic Signal',
                    xaxis_title='Time',
                    yaxis_title='Amplitude')
    return fig


@app.callback(
    [
        Output('amplitude-input', 'value'),
        Output('frequency-input', 'value'),
        Output('phase-input', 'value'),
        Output('noise-mean-input', 'value'),
        Output('noise-covariance-input', 'value'),
        Output('show-noise-switch', 'on'),
        Output('show-filter-switch', 'on'),
        Output('filter-cutoff', 'value'),
        Output('filter-fs', 'value'),
    ],
    [Input('reset-button', 'n_clicks')]
)
def reset_inputs(n_clicks):
    default_values = {
        'amplitude-input': 1,
        'frequency-input': 1,
        'phase-input': 0,
        'noise-mean-input': 0,
        'noise-covariance-input': 0.1,
        'show-noise-switch': True,
        'show-filter-switch': False,
        'filter-cutoff': 0.5,
        'filter-fs': 30,
    }
    return [default_values[input_id] for input_id in default_values]


if __name__ == '__main__':
    app.run_server(debug=True)
