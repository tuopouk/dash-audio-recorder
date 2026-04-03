import dash_audio_recorder
from dash import Dash, html, dcc, Input, Output, State, callback

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H2("Audio Quality & Streaming Test Bench"),
    html.P("Test browser filters and the new live streaming mode."),
    
    # Asetuspaneeli
    html.Div([
        html.Label("1. Browser Filters (Disable for AI/Whisper):", style={'fontWeight': 'bold'}),
        dcc.Checklist(
            id='audio-filters',
            options=[
                {'label': ' Echo Cancellation', 'value': 'echo'},
                {'label': ' Noise Suppression', 'value': 'noise'},
                {'label': ' Auto Gain Control', 'value': 'gain'}
            ],
            value=[], 
            style={'marginTop': '5px', 'marginBottom': '20px'}
        ),

        html.Label("2. Recording Mode:", style={'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='stream-toggle',
            options=[
                {'label': ' Normal Mode (Wait until stopped)', 'value': 'normal'},
                {'label': ' Stream Mode (Live 1-second chunks)', 'value': 'stream'}
            ],
            value='normal', # Oletuksena normaali tila
            style={'marginTop': '5px'}
        )
    ], style={'backgroundColor': '#f0f0f0', 'padding': '15px', 'borderRadius': '8px', 'marginBottom': '20px'}),

    # Komponentti ladataan tähän diviin dynaamisesti
    html.Div(id='recorder-container'),
    
    # Tuloste: Normaali tila
    html.Div([
        html.H4("Normal Mode Output:", style={'marginTop': '0'}),
        html.Div(id='status-message', style={'fontWeight': 'bold'}),
        html.Audio(id='audio-player', controls=True, style={'marginTop': '10px', 'width': '100%'})
    ], style={'marginTop': '20px', 'padding': '15px', 'border': '1px solid #ccc', 'borderRadius': '8px'}),

    # Tuloste: Striimaustila (Terminaali-tyylinen)
    html.Div([
        html.H4("Stream Mode Output (Live):", style={'marginTop': '0'}),
        html.Pre(id='live-stream-output', style={
            'backgroundColor': '#2c3e50', 'color': '#4aed88', 'padding': '15px',
            'height': '150px', 'overflowY': 'scroll', 'borderRadius': '8px',
            'fontFamily': 'monospace', 'margin': '0'
        })
    ], style={'marginTop': '20px'})
    
], style={'padding': '40px', 'fontFamily': 'sans-serif', 'maxWidth': '600px', 'margin': '0 auto'})


# 1. Callback: Luo komponentin uusilla asetuksilla
@callback(
    Output('recorder-container', 'children'),
    Input('audio-filters', 'value'),
    Input('stream-toggle', 'value')
)
def update_recorder(filters, mode):
    return dash_audio_recorder.DashAudioRecorder(
        id='audio-recorder',
        visualMode='fullscreen', 
        recordMode='click', # Click on kätevin striimiä testatessa
        echoCancellation='echo' in filters,
        noiseSuppression='noise' in filters,
        autoGainControl='gain' in filters,
        streamMode=(mode == 'stream') # TÄMÄ kytkee striimauksen päälle/pois
    )

# 2. Callback: Käsittelee kokonaisen äänen (Normaali tila)
@callback(
    Output('audio-player', 'src'),
    Output('status-message', 'children'),
    Input('audio-recorder', 'audioData')
)
def process_normal_audio(audio_data):
    if not audio_data:
        return "", "Waiting for recording in Normal Mode..."
    
    return audio_data, "Recording complete! Listen below:"

# 3. Callback: Käsittelee reaaliaikaiset palaset (Striimaustila)
@callback(
    Output('live-stream-output', 'children'),
    Input('audio-recorder', 'audioStream'),
    State('live-stream-output', 'children'),
    State('stream-toggle', 'value')
)
def process_stream_audio(audio_chunk, existing_text, mode):
    if mode != 'stream':
        return "Switch to Stream Mode to see live data chunks arriving here."
    
    if not audio_chunk:
        return "Waiting for live audio stream..."
    
    # Luodaan logirivi uudelle palaselle
    new_log = f"[LIVE] Received chunk: {len(audio_chunk)} bytes"
    
    # Lisätään uusi rivi vanhojen yläpuolelle (tai alle)
    if existing_text and "[LIVE]" in existing_text:
        return f"{new_log}\n{existing_text}"
    
    return new_log

if __name__ == '__main__':
    app.run(debug=True)