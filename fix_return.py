import re

with open('sky_doodles/init.lua', 'r') as f:
    content = f.read()

# Replace `return true -- return true to skip Mobs Redo default movement/physics` with `return false`
content = content.replace("return true -- return true to skip Mobs Redo default movement/physics", "return false -- return false to skip Mobs Redo default movement/physics")

with open('sky_doodles/init.lua', 'w') as f:
    f.write(content)
