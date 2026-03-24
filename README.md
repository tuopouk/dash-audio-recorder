# Dash Audio Recorder

A professional and customizable audio recording component for Plotly Dash. This component allows users to record audio directly from their browser's microphone, visualize the audio as a waveform in real-time, and send the data back to Python for processing.

**🔥 AI / Whisper Optimization!** You can disable the browser's default audio filters (noise suppression, echo cancellation, auto gain) to capture pure, raw acoustic data. This dramatically improves speech recognition accuracy for AI models like OpenAI's Whisper.

## Key Features

* **AI-Ready Audio:** Option to capture raw, unfiltered audio (128 kbps) for maximum ASR (Automatic Speech Recognition) accuracy.
* **Real-time Waveform:** Visualize audio input as it happens.
* **Two UI Modes:** Support for both a discrete `small` view and an immersive `fullscreen` recording experience.
* **Flexible Interaction:** Choose between `hold` (Push-To-Talk) or `click` (Toggle) to control recording.
* **Memory Efficient:** Sends audio data as a Base64 string directly to Dash, allowing for lightning-fast handling via `dcc.Store` or temporary files without mandatory disk writes.

## Installation

Install the package via pip:

```bash
pip install dash-audio-recorder
```

## Quick Start (Usage Example)

Here is a complete example showing how to use the component, optimized for testing audio quality with AI models like Whisper. Save this as `usage.py` and run it to test the component locally.

```python
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
        recordMode='click', # Using 'click' for toggle mode instead of 'hold'
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
    # Modern Dash uses app.run instead of app.run_server
    app.run(debug=True)
```

## Component Properties (Props)

| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`id`** | `string` | `None` | The ID used to identify this component in Dash callbacks. |
| **`audioData`** | `string` | `None` | The recorded audio data as a Base64 encoded string. Read-only from Python. |
| **`audioType`** | `string` | `'audio/webm'` | The MIME type for the audio recording (e.g., `audio/webm`, `audio/mp4`). |
| **`visualMode`** | `string` | `'fullscreen'` | UI style: `'fullscreen'` (overlay) or `'small'` (inline block). |
| **`recordMode`** | `string` | `'hold'` | Interaction style: `'hold'` (push-to-talk) or `'click'` (toggle on/off). |
| **`echoCancellation`**| `boolean`| `False` | Whether to use the browser's echo cancellation. Keep `False` for AI usage. |
| **`noiseSuppression`**| `boolean`| `False` | Whether to use the browser's noise suppression. Keep `False` for AI usage. |
| **`autoGainControl`** | `boolean`| `False` | Whether to automatically adjust microphone volume. Keep `False` for AI usage. |

## License

This project is licensed under the MIT License.