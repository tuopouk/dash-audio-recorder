import dash_audio_recorder
from dash import Dash, html, dcc, Input, Output, State, callback
import base64
import os

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Ammattimainen äänitin"),
    
    # 1. VALINTAKYTKIN: Miten ääni halutaan käsitellä
    html.Div([
        html.Label("Valitse käsittelytapa:", style={'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='save-mode',
            options=[
                {'label': ' Pidä vain välimuistissa (Nopea, menee dcc.Storeen)', 'value': 'memory'},
                {'label': ' Tallenna kovalevylle (Luo fyysisen tiedoston)', 'value': 'disk'}
            ],
            value='memory', # Oletuksena käytetään nopeaa muistia
            style={'marginBottom': '30px', 'marginTop': '10px'}
        )
    ]),
    
    html.P("Pidä mikrofonia pohjassa äänittääksesi."),
    
    dash_audio_recorder.DashAudioRecorder(
        id='audio-recorder',
        audioType='audio/webm',
        visualMode='fullscreen',  # Aalto koko ruudulla
        recordMode='hold'         # 'hold' toimii nyt oikein!
    ),
    
    # Store, johon data menee aina käytettäväksi myöhemmin
    dcc.Store(id='audio-memory-store'),
    
    html.Div(id='status-message', style={'marginTop': '40px', 'marginBottom': '20px', 'fontWeight': 'bold'}),
    
    html.Audio(id='audio-player', controls=True, style={'display': 'none'})
    
], style={'padding': '50px', 'textAlign': 'center', 'fontFamily': 'sans-serif'})


@callback(
    Output('audio-memory-store', 'data'),
    Output('audio-player', 'src'),
    Output('audio-player', 'style'),
    Output('status-message', 'children'),
    Input('audio-recorder', 'audioData'),
    State('save-mode', 'value') # Otetaan valintakytkimen arvo mukaan State-muuttujana
)
def process_audio(audio_data, save_mode):
    if audio_data is None:
        return None, "", {'display': 'none'}, "Odotetaan äänitystä..."

    status_text = ""

    # Jos käyttäjä valitsi kovalevylle tallennuksen
    if save_mode == 'disk':
        try:
            header, encoded = audio_data.split(",", 1)
            decoded_audio = base64.b64decode(encoded)
            
            # Päätellään pääte
            extension = "webm"
            if "mp4" in header:
                extension = "mp4"
                
            filename = f"tallennettu_aani.{extension}"
            with open(filename, "wb") as f:
                f.write(decoded_audio)
                
            status_text = f"Äänitys tallennettu kovalevylle tiedostoksi: {os.path.abspath(filename)}"
        except Exception as e:
            status_text = f"Virhe tiedoston tallennuksessa: {e}"
            
    # Jos valittiin nopea muisti (Store)
    else:
        status_text = "Äänitys valmis! Käsitelty vain muistissa (ei luotu tiedostoa)."

    # Palautetaan data aina Storelle ja HTML-soittimelle, riippumatta tallennustavasta
    return (
        audio_data,                         # dcc.Store
        audio_data,                         # html.Audio src
        {'display': 'inline-block'},        # html.Audio style
        status_text                         # Ilmoitusteksti
    )

if __name__ == '__main__':
    app.run(debug=True)