def load_ir_file(file_path):
    ir_file = open(file_path, 'r')

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

    requested_cmd = input('Command name to be traced: ')

    if requested_cmd not in section_dict.keys():
        print('Error: This command is not in the provided file')
        exit()

    return section_dict, requested_cmd