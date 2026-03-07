# Dash Audio Recorder

A professional and customizable audio recording component for Plotly Dash. This component allows users to record audio directly from their browser's microphone, visualize the audio as a waveform in real-time, and send the data back to Python for processing.



## Key Features

* **Real-time Waveform:** Visualize audio input as it happens.
* **Two UI Modes:** Support for both a discrete `small` view and an immersive `fullscreen` recording experience.
* **Flexible Interaction:** Choose between `hold` (Push-To-Talk) or `click` to toggle recording modes.
* **Memory Efficient:** Sends audio data as a Base64 string directly to Dash, allowing for lightning-fast handling via `dcc.Store` without mandatory disk writes.
* **Customizable Formats:** Specify preferred MIME types (e.g., `audio/webm`, `audio/mp4`).

## Installation

Install the package via pip:

```bash
pip install dash-audio-recorder


### Quick Start
Here is a minimal example of how to use the component in a Dash application.

import dash_audio_recorder
from dash import Dash, html, Input, Output, callback

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Dash Audio Recorder Demo"),
    
    dash_audio_recorder.DashAudioRecorder(
        id='audio-recorder',
        audioType='audio/webm',
        visualMode='fullscreen',  # Options: 'fullscreen', 'small'
        recordMode='hold'         # Options: 'hold', 'click'
    ),
    
    html.Div(id='output-status', style={'marginTop': '20px'}),
    html.Audio(id='audio-player', controls=True, style={'marginTop': '10px'})
])

@callback(
    Output('audio-player', 'src'),
    Output('output-status', 'children'),
    Input('audio-recorder', 'audioData')
)
def handle_audio(audio_data):
    if not audio_data:
        return "", "Waiting for recording..."
    
    # audio_data is a base64 string that can be used directly as a source
    return audio_data, "Recording received! You can play it back below:"

if __name__ == '__main__':
    app.run_server(debug=True)


### Component Properties (Props)


Prop,Type,Default,Description
id,string,None,The ID used to identify this component in Dash callbacks.
audioData,string,None,The recorded audio data as a Base64 encoded string. Read-only from Python.
audioType,string,'audio/webm',"The MIME type for the audio recording (e.g., audio/webm, audio/mp4)."
visualMode,string,'fullscreen',UI style: 'fullscreen' (overlay) or 'small' (inline block).
recordMode,string,'hold',Interaction style: 'hold' (push-to-talk) or 'click' (toggle).

### License
This project is licensed under the MIT License.
