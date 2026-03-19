# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class DashAudioRecorder(Component):
    """A DashAudioRecorder component.


Keyword arguments:

- id (string; optional)

- audioData (string; optional)

- audioType (string; default 'audio/webm')

- autoGainControl (boolean; default False)

- echoCancellation (boolean; default False)

- noiseSuppression (boolean; default False)

- recordMode (string; default 'hold')

- visualMode (string; default 'fullscreen')"""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_audio_recorder'
    _type = 'DashAudioRecorder'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        audioData: typing.Optional[str] = None,
        audioType: typing.Optional[str] = None,
        visualMode: typing.Optional[str] = None,
        recordMode: typing.Optional[str] = None,
        echoCancellation: typing.Optional[bool] = None,
        noiseSuppression: typing.Optional[bool] = None,
        autoGainControl: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'audioData', 'audioType', 'autoGainControl', 'echoCancellation', 'noiseSuppression', 'recordMode', 'visualMode']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'audioData', 'audioType', 'autoGainControl', 'echoCancellation', 'noiseSuppression', 'recordMode', 'visualMode']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashAudioRecorder, self).__init__(**args)

setattr(DashAudioRecorder, "__init__", _explicitize_args(DashAudioRecorder.__init__))
