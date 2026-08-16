with open('sky_doodles/init.lua', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("-- Implement do_custom"):
        break
    new_lines.append(line)

with open('sky_doodles/init.lua', 'w') as f:
    f.writelines(new_lines)
