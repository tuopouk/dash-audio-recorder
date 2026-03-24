import dash_audio_recorder
from dash import Dash, html, dcc, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Audio Quality Test Bench (Whisper Optimization)"),
    html.P("Test how the audio sounds with and without browser filters (raw audio)."),
    
    # Selection menus for toggling filters
    html.Div([
        html.Label("Browser Filters (Try disabling all for Whisper):", style={'fontWeight': 'bold'}),
        dcc.Checklist(
            id='audio-filters',
            options=[
                {'label': ' Echo Cancellation', 'value': 'echo'},
                {'label': ' Noise Suppression', 'value': 'noise'},
                {'label': ' Auto Gain Control', 'value': 'gain'}
            ],
            value=[], # Default empty = all filters OFF (raw audio)
            style={'marginTop': '10px'}
        )
    ], style={'backgroundColor': '#f0f0f0', 'padding': '15px', 'borderRadius': '8px', 'marginBottom': '20px'}),

    # The recorder component is loaded into this div dynamically
    html.Div(id='recorder-container'),
    
    html.Div(id='status-message', style={'marginTop': '20px', 'fontWeight': 'bold'}),
    html.Audio(id='audio-player', controls=True, style={'marginTop': '10px'})
    
], style={'padding': '40px', 'fontFamily': 'sans-serif', 'maxWidth': '600px', 'margin': '0 auto'})


# This callback recreates the recorder whenever filter settings are changed
@callback(
    Output('recorder-container', 'children'),
    Input('audio-filters', 'value')
)
def update_recorder(filters):
    return dash_audio_recorder.DashAudioRecorder(
        id='audio-recorder',
        visualMode='fullscreen', 
        recordMode='hold',
        echoCancellation='echo' in filters,
        noiseSuppression='noise' in filters,
        autoGainControl='gain' in filters
    )

# This callback receives the audio data and passes it to the player
@callback(
    Output('audio-player', 'src'),
    Output('status-message', 'children'),
    Input('audio-recorder', 'audioData')
)
def process_audio(audio_data):
    if not audio_data:
        return "", "Press the microphone and speak to start testing."
    
    return audio_data, "Recording complete! Listen to the differences by toggling filters."

if __name__ == '__main__':
    app.run(debug=True)