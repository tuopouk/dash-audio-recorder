import dash_audio_recorder
from dash import Dash, html, dcc, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Äänenlaadun testipenkki (Whisper-optimointi)"),
    html.P("Testaa, miltä ääni kuulostaa selaimen suodattimilla ja ilman (raakana)."),
    
    # Valikot filttereiden päälle/pois laittamiseen
    html.Div([
        html.Label("Selaimen suodattimet (Kokeile ottaa kaikki pois Whisperille):", style={'fontWeight': 'bold'}),
        dcc.Checklist(
            id='audio-filters',
            options=[
                {'label': ' Kaiunpoisto (Echo Cancellation)', 'value': 'echo'},
                {'label': ' Taustakohinan vaimennus (Noise Suppression)', 'value': 'noise'},
                {'label': ' Automaattinen tasonsäätö (Auto Gain)', 'value': 'gain'}
            ],
            value=[], # Oletuksena tyhjä = kaikki filtterit POIS (raaka ääni)
            style={'marginTop': '10px'}
        )
    ], style={'backgroundColor': '#f0f0f0', 'padding': '15px', 'borderRadius': '8px', 'marginBottom': '20px'}),

    # Komponentti ladataan tähän diviin dynaamisesti
    html.Div(id='recorder-container'),
    
    html.Div(id='status-message', style={'marginTop': '20px', 'fontWeight': 'bold'}),
    html.Audio(id='audio-player', controls=True, style={'marginTop': '10px'})
    
], style={'padding': '40px', 'fontFamily': 'sans-serif', 'maxWidth': '600px', 'margin': '0 auto'})


# Tämä callback luo äänittimen uudestaan aina, kun muutat filttereiden asetuksia
@callback(
    Output('recorder-container', 'children'),
    Input('audio-filters', 'value')
)
def update_recorder(filters):
    return dash_audio_recorder.DashAudioRecorder(
        id='audio-recorder',
        visualMode='fullscreen', # Pidetään pienenä testin ajan
        recordMode='hold',
        echoCancellation='echo' in filters,
        noiseSuppression='noise' in filters,
        autoGainControl='gain' in filters
    )

# Tämä callback ottaa äänen vastaan ja laittaa sen soittimeen
@callback(
    Output('audio-player', 'src'),
    Output('status-message', 'children'),
    Input('audio-recorder', 'audioData')
)
def process_audio(audio_data):
    if not audio_data:
        return "", "Paina mikrofonia ja puhu jotain testataksesi."
    
    return audio_data, "Äänitys valmis! Kuuntele erot laittamalla filttereitä päälle/pois."

if __name__ == '__main__':
    app.run(debug=True)
