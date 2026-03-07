# AUTO GENERATED FILE - DO NOT EDIT

#' @export
''DashAudioRecorder <- function(id=NULL, audioData=NULL, audioType=NULL, recordMode=NULL, visualMode=NULL) {
    
    props <- list(id=id, audioData=audioData, audioType=audioType, recordMode=recordMode, visualMode=visualMode)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashAudioRecorder',
        namespace = 'dash_audio_recorder',
        propNames = c('id', 'audioData', 'audioType', 'recordMode', 'visualMode'),
        package = 'dashAudioRecorder'
        )

    structure(component, class = c('dash_component', 'list'))
}
