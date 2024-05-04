import matplotlib.pyplot as plt

FILE_PATH = 'assets/Climatisation_avignon.ir'
ir_file = open(FILE_PATH, 'r')

first_marker = False
sections = [""]
current_section = -1
for line in ir_file.readlines():
    if line.startswith('#'):
        sections[current_section] = sections[current_section].rstrip('\n ')
        current_section += 1
        continue

    if current_section >= 0:
        if len(sections) < current_section + 1:
            sections += [""]
        sections[current_section] += line

# For the last line
sections[current_section] = sections[current_section].rstrip('\n ')

section_dict = {}
for section in sections:
    section_split = section.split('\n')
    section_description = {}
    for raw_line in section_split:
        [key, value] = raw_line.split(': ')
        section_description[key] = value
    section_dict[section_description['name']] = section_description

print('Available commands:')
key_list = ""
for key in section_dict.keys():
    key_list += key + ', '
print(key_list.rstrip(', '))

requested_cmd = input('Command name to be prepared: ')

if requested_cmd not in section_dict.keys():
    print('Error: This command is not in the provided file')
    exit()

data_requested = section_dict[requested_cmd]['data']
raw_data = [int(data) for data in data_requested.split(' ')]
payload_length = len(raw_data)

payload = []
current_state = True
for data in raw_data:
    payload += [{'duration': str(data), 'state': 1 if current_state else 0}]
    current_state = not current_state

print("Payload length: " + str(payload_length))
print(payload)

print('\n\nCode associé: ')
generated_code = ""
generated_code += 'SD_IRState payload[' + str(payload_length) + '];\n'

for k in range(payload_length):
    generated_code += 'payload[' + str(k) + '].duration = ' + payload[k]['duration'] + ';\n'
    generated_code += 'payload[' + str(k) + '].state = ' + str(payload[k]['state']) + ';\n'
    generated_code += '\n'

generated_code_file_path = 'out/generated_code.c'
generated_code_file = open(generated_code_file_path, 'w')
generated_code_file.writelines(generated_code)

print(generated_code)
print('Saved as out/generated_code.c')
