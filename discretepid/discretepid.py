import time

def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value

class PID(object):

    def __init__(
        self,
        Kp=1.0,
        Ti=0.0,
        Td=0.0,
        N=0,
        setpoint=0,
        sample_time=0.01,
        output_limits=(None, None),
        auto_mode=True,
        ramping_rate = None,
        variable_setpoint = 0
        ):

        self.Kp, self.Ti, self.Td, self.N = Kp, Ti, Td,N
        self.setpoint = setpoint
        self.sample_time = sample_time

        self._min_output, self._max_output = None, None
        self._auto_mode = auto_mode
        
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = None
        self._last_output = None
        self._last_error = 0
        self._last_input = None
        self._start_setpoint= 0
        self.ramping_rate= ramping_rate
        self._on_change = True
        self.start_time = None
        self.variable_setpoint = variable_setpoint
        self.prev_setpoint = 0
        
        try:
            self.time_fn = time.monotonic
        except AttributeError:
            self.time_fn = time.time

        self.output_limits = output_limits
        self.reset()
    
    def __call__(self,input_,dt=None):
        if not self.auto_mode:
            return self._last_output

        now = self.time_fn()
        if dt is None:
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError('dt has negative value {}, must be positive'.format(dt))

        if self.ramping_rate is not None:
            if self.ramping_rate < 0:
                raise ValueError('ramping_rate has negative value {}, must be positive'.format(self.ramping_rate))
            elif round(self.ramping_rate) == 0:
                self.ramping_rate = None

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            return self._last_output

        if self.setpoint != self._start_setpoint and self.ramping_rate is not None and self._on_change:
            self.start_time = time.time()
            self._on_change = False

        if self.start_time is not None and self.ramping_rate is not None:
            if not self._on_change and self.variable_setpoint != self.setpoint and self.prev_setpoint != self.setpoint:
                self._start_setpoint = self.variable_setpoint
                self.prev_setpoint = self.setpoint
                self.start_time = time.time()

            if time.time() - self.start_time <= self.ramping_rate :
                dy = (abs(self.setpoint - self._start_setpoint))/(self.ramping_rate/dt)
                if self.setpoint >= self._start_setpoint:
                    self.variable_setpoint = self.variable_setpoint + dy
                    self.variable_setpoint = _clamp(self.variable_setpoint, (self._start_setpoint,self.setpoint))
                else:
                    self.variable_setpoint = self.variable_setpoint - dy
                    self.variable_setpoint = _clamp(self.variable_setpoint, (self.setpoint,self._start_setpoint))

            elif time.time() - self.start_time > self.ramping_rate:
                self._start_setpoint = self.variable_setpoint
                self._on_change = True
                self.start_time = None

        #Error Calculation
        if self.ramping_rate is None: 
            error = self.setpoint - input_
        else:
            error = self.variable_setpoint - input_
        d_error = error - (self._last_error if (self._last_error is not None) else error)
        
        #Proportional term
        self._proportional= self.Kp*error
        
        #Integrative term
        if self.Ti != 0: 
            self._integral += ((self.Kp*dt)/self.Ti)*error
            self._integral = _clamp(self._integral, self.output_limits)
        
        #Derivative term
        if self.Td !=0:
            self._derivative= (self.Td/(self.N*dt+self.Td))*self._derivative + ((self.Kp*self.Td*self.N)/(self.N*dt+self.Td))*d_error
                   
        # Output Calculation
        output = self._proportional + self._integral + self._derivative
        output = _clamp(output, self.output_limits)

        # Update PID state
        self._last_output = output
        self._last_error = error
        self._last_time = now
        
        return output
    
    @property
    def auto_mode(self):
        """Whether the controller is currently enabled or not."""
        return self._auto_mode

    @property
    def components(self):
        """ Values Kp,Ti,Td,N,ramping_rate
        """
        return self.Kp, self.Ti, self.Td,self.N, self.ramping_rate
    @property
    def tunings(self):
        """The tunings used by the controller """
        return self.Kp, self.Ti, self.Td,self.N, self.setpoint

    @tunings.setter
    def tunings(self, tunings):
        """Set the PID tunings."""
        self.Kp, self.Ti , self.Td ,self.N, self.setpoint = tunings
    
    @auto_mode.setter
    def auto_mode(self, enabled):
        """Enable or disable the PID controller"""
        self.set_auto_mode(enabled)
        
    def set_auto_mode(self, enabled, last_output=None):
        """ Enable or disable the PID controller, optionally setting the last output value."""
        if enabled and not self._auto_mode:
            self.reset()

            self._integral = last_output if (last_output is not None) else 0
            self._integral = _clamp(self._integral, self.output_limits)

        self._auto_mode = enabled
        
    def output_limits(self, limits):
        """Set Output Limits"""
        if limits is None:
            self._min_output, self._max_output = None, None
            return

        min_output, max_output = limits

        if (None not in limits) and (max_output < min_output):
            raise ValueError('lower limit must be less than upper limit')

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        self._last_output = _clamp(self._last_output, self.output_limits)
        
    def reset(self):
        """ Reset PID controller """
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._integral = _clamp(self._integral, self.output_limits)

        self._last_time = self.time_fn()
        self._last_output = None
        self._last_input = None


    def change_setpoint(self,new_setpoint):
        """Change setpoint"""
        self.prev_setpoint = self.setpoint
        self.setpoint = new_setpoint

    def reset_ramping_rate(self):
        """Reset ramp duration"""
        self.ramping_rate = None
