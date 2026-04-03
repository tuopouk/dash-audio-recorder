# AUTO GENERATED FILE - DO NOT EDIT

export ''_dashaudiorecorder

"""
    ''_dashaudiorecorder(;kwargs...)

A DashAudioRecorder component.

Keyword arguments:
- `id` (String; optional)
- `audioData` (String; optional)
- `audioStream` (String; optional)
- `audioType` (String; optional)
- `autoGainControl` (Bool; optional)
- `currentVolume` (Real; optional)
- `echoCancellation` (Bool; optional)
- `noiseSuppression` (Bool; optional)
- `recordMode` (String; optional)
- `streamMode` (Bool; optional)
- `visualMode` (String; optional)
"""
function ''_dashaudiorecorder(; kwargs...)
        available_props = Symbol[:id, :audioData, :audioStream, :audioType, :autoGainControl, :currentVolume, :echoCancellation, :noiseSuppression, :recordMode, :streamMode, :visualMode]
        wild_props = Symbol[]
        return Component("''_dashaudiorecorder", "DashAudioRecorder", "dash_audio_recorder", available_props, wild_props; kwargs...)
end

