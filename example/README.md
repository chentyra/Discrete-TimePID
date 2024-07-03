# Water Boiler Example
Simple simulation of a water boiler which can heat up water and where the heat dissipates slowly over time. Running the example will run the water boiler simulation for 30 seconds and use the PID controller to make the boiler reach a setpoint temperature. The results will also be plotted using Matplotlib.

This folder provides various examples to illustrate the usage and capabilities of the PID controller. It includes three specific examples:

- `example_step.py`: Demonstrates the controller's behavior with a step reference input.

- `example_ramping.py`: Showcases the controller's behavior with a ramp reference input.

- `example_mix.py`: Illustrates how to transition from a ramp reference input to a step reference input.

## example_step.py
The outcomes of this example demonstrate how the PID controller achieves three distinct setpoints in response to a step reference input.

![example1](https://github.com/chentyra/Discrete-TimePID/assets/68944703/f4233541-6904-40e2-9ea0-e6e23641c153)

## example_ramping.py
This example showcases how the PID controller achieves three distinct setpoints in response to a ramp reference input with a duration of five seconds. The ramp duration can be dynamically modified as per the instructions provided on the main page.

![example2](https://github.com/chentyra/Discrete-TimePID/assets/68944703/fa38eb92-51e5-450f-a348-2d30dcbe1177)

## example_mix.py
This example demonstrates how to dynamically transition between a ramp reference input and a step reference input using the `reset_ramping_rate()` instruction. The inverse operation is also valid.

![example3](https://github.com/chentyra/Discrete-TimePID/assets/68944703/0fba5b8a-b701-4a30-a082-8c53e725f7f9)
