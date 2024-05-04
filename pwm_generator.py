import matplotlib.pyplot as plt


def pwm(frequency, cyclic, duration, offset = 0):
    period = 1/frequency
    period_high = period * cyclic

    pattern_x = [offset, offset + period_high, offset + period_high + period * 0.001, offset + period]
    pattern_y = [1, 1, 0, 0]

    global_x = []
    global_y = []
    for k in range(0, int(duration / period)):
        global_x += [pattern_x[0] + k*period, pattern_x[1] + k*period, pattern_x[2] + k*period, pattern_x[3] + k*period]
        global_y += pattern_y

    return global_x, global_y


def pwm_converter(signal, frequency, cyclic):
    high_period = 1/frequency * cyclic
    period = 1/frequency
    pwm_list = []

    for sig in signal:
        if sig / period > 1:
            # If signal contains more than a period, it's probably a
            # repetitive period with cyclic = 1
            for k in range(int(sig / high_period)):
                pwm_list += [0]
        else:
            pwm_list += [cyclic]
    return pwm_list


'''
    Get the duty-cycle to reproduce the <pattern> with a pwm value of the specified <frequency>
'''
def local_pwm_converter(pattern):
    high_period = 0
    for value in pattern:
        if value > 0:
            high_period += 1
    return high_period / len(pattern)

def pwm_generate_signal(frequency, duty_cycles):
    signal_x = []
    signal_y = []

    offset = 0
    for duty_cycle in duty_cycles:
        x, y = pwm(frequency, duty_cycle, 1 / frequency, offset)
        signal_x += x
        signal_y += y

        offset += 1 / frequency

    return signal_x, signal_y


'''
Convert a signal to a list of duty cycles for pwm signal with the provided frequency
signal = (signal_x, signal_y)
'''
def signal_to_pwm(signal, frequency):
    signal_x, signal_y = signal
    last_split = 0
    splitted_signal = []
    nb_points_per_period = int(1 / frequency * 1000000)
    for k in range(int(len(signal_x) / (1 / frequency * 1000000))):
        x_split = signal_x[last_split:last_split + nb_points_per_period]
        y_split = signal_y[last_split:last_split + nb_points_per_period]
        splitted_signal.append([x_split, y_split])
        last_split += nb_points_per_period

    pwm_list = []
    for pattern in splitted_signal:
        pwm_list += [local_pwm_converter(pattern[1])]

    return pwm_list



# [pwm_x, pwm_y] = pwm(1200, 0.64, 0.132625)

# print(pwm_x)

# plt.plot(pwm_x, pwm_y)
# plt.ylim((-5, 5))
# plt.show()

