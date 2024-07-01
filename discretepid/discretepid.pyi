from typing import Callable, Optional, Tuple

_Limits = Tuple[Optional[float], Optional[float]]
_Components = Tuple[float, float, float,float, float, Optional[float]]
_Tunings = Tuple[float, float, float,float, float]

def _clamp(value: Optional[float], limits: _Limits) -> Optional[float]: ...

class PID(object):
    Kp: float
    Ti: float
    Td: float
    N: float
    setpoint: float
    sample_time: Optional[float]
    time_fn: Callable[[], float]
    def __init__(
        self,
        Kp: float = ...,
        Ti: float = ...,
        Td: float = ...,
        N: float= ...,
        setpoint: float = ...,
        sample_time: Optional[float] = ...,
        output_limits: _Limits = ...,
        auto_mode: bool = ...,
        ramping_rate: Optional[float] = ...,
        variable_setpoint: Optional[float] = ...,
    ) -> None: ...
    
    def __call__(self, input_: float, dt: Optional[float] = ...) -> Optional[float]: ...
    @property
    def auto_mode(self) -> bool: ...
    @property
    def components(self) -> _Components: ...
    @property
    def tunings(self) -> _Tunings: ...
    @tunings.setter
    def tunings(self, tunings: _Tunings) -> None: ...
    @auto_mode.setter
    def auto_mode(self, enabled: bool) -> None: ...
    def set_auto_mode(self, enabled: bool, last_output: Optional[float] = ...) -> None: ...
    @property
    def output_limits(self) -> _Limits: ...
    @output_limits.setter
    def output_limits(self, limits: _Limits) -> None: ...
    def reset(self) -> None: ...
    def change_setpoint(self,new_setpoint: float)-> None: ...
    def reset_ramping_rate(self) -> None: ...
