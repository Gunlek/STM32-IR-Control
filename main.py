import matplotlib.pyplot as plt
from pwm_generator import pwm_generate_signal, local_pwm_converter, signal_to_pwm
import utils
import assets.path
import numpy as np

ir_dict, requested_cmd = utils.load_ir_file(assets.path.FILE_PATH)

data_requested = ir_dict[requested_cmd]['data']
sum_of_steps = 0
raw_data = [int(raw_data) for raw_data in data_requested.split(' ')]
for interval in raw_data:
    sum_of_steps += interval

x_signal = [x for x in range(sum_of_steps)]
y_signal = []

current_state = True
lin_duration = np.linspace(0, sum_of_steps / 1000000, sum_of_steps)
for duration in raw_data:
    int_duration = int(duration)
    for k in range(int_duration):
        y_signal += [1 if current_state else 0]
    current_state = not current_state

print('Payload length: ' + str(sum_of_steps))

frequency = 1226    # Frequency of the PWM signal

# Split the signals per frequency (to see the duty-cycles)
last_split = 0
splitted_signal = []
nb_points_per_period = int(1 / frequency * 1000000)
for k in range(int(sum_of_steps / (1 / frequency * 1000000))):
    x_split = lin_duration[last_split:last_split + nb_points_per_period]
    y_split = y_signal[last_split:last_split + nb_points_per_period]
    splitted_signal.append([x_split, y_split])
    last_split += nb_points_per_period

    plt.plot(x_split, y_split)

# Convert the signal to a list of duty-cycles at a specific frequency
duty_cycles = signal_to_pwm((lin_duration, y_signal), frequency)

# Generated a signal from PWM duty-cycles list
generated_signal_x, generated_signal_y = pwm_generate_signal(frequency, duty_cycles)
plt.plot(generated_signal_x, generated_signal_y)

print('Corresponding Duty-Cycles at ' + str(frequency) + 'Hz: ')
print(duty_cycles)

plt.ylim((-5, 5))
plt.show()


