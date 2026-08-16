with open('sky_doodles/init.lua', 'r') as f:
    content = f.read()

import re
content = content.replace("mobs:spawn({", "mobs:register_spawn({")

with open('sky_doodles/init.lua', 'w') as f:
    f.write(content)
