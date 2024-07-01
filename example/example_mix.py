import sys
import time
import matplotlib.pyplot as plt
from discretepid import PID

class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """

    def __init__(self):
        self.water_temp = 20

    def update(self, boiler_power, dt):
        if boiler_power > 0:
            # Boiler can only produce heat, not cold
            self.water_temp += 1 * boiler_power * dt

        # Some heat dissipation
        self.water_temp -= 0.02 * dt
        return self.water_temp


if __name__ == '__main__':
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(15, 10, 0.01, N=5, setpoint=40, ramping_rate= 5)
    pid.output_limits = (0, 100)

    start_time = time.time()
    print_time = time.time()
    last_time = start_time

    # Keep track of values for plotting
    setpoint, output,input, t = [], [], [], []

    time_simulation = 30

    print("Simulation duration: " + str(time_simulation))

    while time.time() - start_time < time_simulation:
        current_time = time.time()
        dt = current_time - last_time

        power = pid(water_temp)
        water_temp = boiler.update(power, dt)

        t += [current_time - start_time]
        output += [water_temp]
        input += [power]

        if pid.ramping_rate is None:
            setpoint += [pid.setpoint]
        else:
            setpoint += [pid.variable_setpoint]

        if current_time - start_time >= 10:
            pid.setpoint = 75

        if current_time - start_time > 20:
            pid.reset_ramping_rate()
            pid.setpoint = 100

        last_time = current_time

        if time.time() - print_time >= 1:
            print = "Current time: " + str(round(time.time() - start_time)) + " seconds"
            sys.stdout.write('\r'+print)
            print_time = time.time()

    print = "Current time: " + str(time_simulation) + " seconds\nGenerating charts..."
    sys.stdout.write('\r' + print)

    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(t, output, label='Measured')
    plt.plot(t, setpoint,'k--', label='Setpoint')
    plt.ylabel('Temperature [°C] ')
    plt.legend(['Measured output', 'Setpoint'], loc="lower right")
    plt.subplot(2,1,2)
    plt.plot(t, input, 'r-')
    plt.xlabel('Time [s]')
    plt.ylabel('Power [%]')
    plt.show()
