# Discrete-Time PID
[![Downloads](https://static.pepy.tech/personalized-badge/realpid?period=total&units=international_system&left_color=grey&right_color=yellow&left_text=downloads)](https://pepy.tech/project/realpid)
![GitHub top language](https://img.shields.io/github/languages/top/chentyra/RealPID) ![GitHub](https://img.shields.io/github/license/chentyra/RealPID?color=orange) ![PyPI](https://img.shields.io/pypi/v/realpid?color=blue) ![GitHub issues](https://img.shields.io/github/issues/chentyra/RealPID?color=red) ![GitHub closed issues](https://img.shields.io/github/issues-closed/chentyra/RealPID) 

An ideal PID is based on the sum of a proportional, integrative and derivative contribution.

$u(t)= K_P(e(t) + \frac{1}{T_I}\int e(\tau)d\tau+ T_D \frac{de}{dt})$

Controller's transfer function $C(s)$ in Laplace domain is not physically achievable.

$C(s)= \frac{u(t)}{e(t)} = K_P (1+ \frac{1}{T_I \cdot s} + T_D \cdot s) = \frac{T_IT_D \cdot s^2 + T_I \cdot s + 1}{T_I \cdot s} $

Furthermore, an ideal PD amplifies measurement noise, and thus might lead to large control signals that can drive the actuator into saturation or might even cause damage. Therefore, it is necessary to filter of the derivative action in the high-frequency by defining a factor N. It usually takes on a value between 5 and 20.

$C(s)=K_P (1+ \frac{1}{T_I \cdot s} + \frac{T_D \cdot s}{1+s \cdot T_D/N})$

A Python implementation of a real PID is provided.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
python -m pip install discretepid
```
## Usage
### Basic Usage

First of all, include the library:
```
from realpid import PID
```
To create PID object, call class's constructor where:
* The first value is **proportional gain** $K_P$
* The second value is **integrative time constant** $T_I$
* The third value is **derivative time constant** $T_D$
* The fourth value is **factor** $N$
* The fifth value is **setpoint** or the value that the PID is trying to achieve
```
pid = PID(1, 0.1, 0.05, 2, setpoint=1)
```
The PID compute a new ```output_value```, on the basis of an ```input_value```, calling the object created.
```
output_value= pid(input_value)
```
### An example

```
from realpid import PID
pid = PID(0.2, 0.6, 0.02, 5, setpoint=1)

while True:
    control = pid(v)
```
### Sample Time

Optionally, a ```sample_time``` can be definied  as last attribute of the instruction which represents the amount of time between one call to another of the updating method:
```
pid.sample_time= 0.01
```
### Output Limit
To avoid integral windup and to limit output value, attribute ```output_limits``` can be set:
```
pid.output_limits = (0, None)  # Output will always be positive, but with no upper bound
```
### Switching On And Off
In order to turn off PID controller, set attribute ```auto_mode``` to False:
```
pid.auto_mode = False
```
In the same way, to turn on PID controller, set attribute ```auto_mode``` to True:
```
pid.auto_mode = True
```
When controlling the system manually, it is useful to set the value of the integral term to the value indicated by the attribute ```last_output```:
```
pid.set_auto_mode(True, last_output=1)
```
## Reset 
The PID controller can be reset calling the ```reset``` method
```
pid.reset()
```
## Other Features 
The value of $K_P$,  $T_I$ , $T_D$ , $N$ can be seen in this way:
```
Kp, Ti, Td,N = pid.components
```
Their values can be changed individually or all at once when the PID is running:
```
pid.Kp = 1.0
pid.tunings = (1.0, 0.3, 0.01, 10)
```
## License
Licensed under the [MIT][def]

[def]: https://choosealicense.com/licenses/mit/
