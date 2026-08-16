with open('sky_doodles/init.lua', 'r') as f:
    content = f.read()

# Replace the incorrect spawn block we just appended
import re
new_content = re.sub(r'-- Custom spawn check function.*', '', content, flags=re.DOTALL)

# Append the correct spawn logic using mobs:register_spawn with custom on_spawn or an ABM.
# The instruction says: "Use `mobs:register_spawn` to spawn it only at `y = 136` in air nodes. Set max per area limit to 10 and low frequency (1% chance). Implement a custom spawn check function to ensure horizontal clearance of 20 nodes"
# `mobs:register_spawn` doesn't support exact Y easily unless we use min_height and max_height.
# Wait, min_height and max_height are parameters!
# The signature is: mobs:register_spawn(name, nodes, max_light, min_light, chance, active_object_count, max_height, day_toggle, on_spawn)
# No, min_height and max_height are often defined by a table in newer mobs redo.
# Let's just use the modern table syntax.
# `mobs:spawn({name="sky_doodles:airplane", nodes={"air"}, min_y=136, max_y=136, chance=100, active_object_count=10, on_spawn=...})`
# Actually, the older table format: `mobs:spawn({name = "...", nodes = {"air"}, min_light = 0, max_light = 15, chance = 100, active_object_count = 10, min_height = 136, max_height = 136, on_spawn = function(self, pos)...})`

custom_logic = """
-- Spawning logic
mobs:spawn({
    name = "sky_doodles:airplane",
    nodes = {"air"},
    min_light = 0,
    max_light = 15,
    chance = 100, -- 1% chance (1 in 100)
    active_object_count = 10,
    min_height = 136,
    max_height = 136,
    on_spawn = function(self, pos)
        local r = 20
        -- Check points around the plane to ensure there are no mountains/buildings
        local checks = {
            {x = pos.x + r, y = pos.y, z = pos.z},
            {x = pos.x - r, y = pos.y, z = pos.z},
            {x = pos.x, y = pos.y, z = pos.z + r},
            {x = pos.x, y = pos.y, z = pos.z - r},
            {x = pos.x + r, y = pos.y, z = pos.z + r},
            {x = pos.x - r, y = pos.y, z = pos.z - r},
            {x = pos.x + r, y = pos.y, z = pos.z - r},
            {x = pos.x - r, y = pos.y, z = pos.z + r},
        }
        for _, p in ipairs(checks) do
            local node = minetest.get_node(p)
            if node and node.name ~= "air" and node.name ~= "ignore" then
                -- Clearance check failed, destroy object
                self.object:remove()
                return false
            end
        end
        return true
    end,
})
"""

with open('sky_doodles/init.lua', 'w') as f:
    f.write(new_content + custom_logic)
