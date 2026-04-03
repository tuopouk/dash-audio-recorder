# AUTO GENERATED FILE - DO NOT EDIT

#' @export
''DashAudioRecorder <- function(id=NULL, audioData=NULL, audioStream=NULL, audioType=NULL, autoGainControl=NULL, currentVolume=NULL, echoCancellation=NULL, noiseSuppression=NULL, recordMode=NULL, streamMode=NULL, visualMode=NULL) {
    
    props <- list(id=id, audioData=audioData, audioStream=audioStream, audioType=audioType, autoGainControl=autoGainControl, currentVolume=currentVolume, echoCancellation=echoCancellation, noiseSuppression=noiseSuppression, recordMode=recordMode, streamMode=streamMode, visualMode=visualMode)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashAudioRecorder',
        namespace = 'dash_audio_recorder',
        propNames = c('id', 'audioData', 'audioStream', 'audioType', 'autoGainControl', 'currentVolume', 'echoCancellation', 'noiseSuppression', 'recordMode', 'streamMode', 'visualMode'),
        package = 'dashAudioRecorder'
        )

    structure(component, class = c('dash_component', 'list'))
}
