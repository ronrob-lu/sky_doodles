import re

with open('sky_doodles/init.lua', 'r') as f:
    content = f.read()

# Replace the closing "})" with our new do_custom and close it.
custom_logic = """
    do_custom = function(self, dtime)
        -- Enforce Y=136 altitude
        local pos = self.object:get_pos()
        if pos then
            if math.abs(pos.y - 136) > 0.1 then
                pos.y = 136
                self.object:set_pos(pos)
            end

            -- Zero out vertical velocity and keep horizontal speed
            local vel = self.object:get_velocity()
            if vel then
                local yaw = self.object:get_yaw() or 0
                local speed = 4 -- 4 nodes/sec forward speed

                -- Calculate forward velocity based on yaw
                -- In Minetest, yaw of 0 is +Z, pi/2 is -X, pi is -Z, 3pi/2 is +X.
                local vx = -math.sin(yaw) * speed
                local vz = math.cos(yaw) * speed

                self.object:set_velocity({x = vx, y = 0, z = vz})
            end
        end

        -- Cloud trail system
        self.trail_timer = (self.trail_timer or 0) + dtime
        if self.trail_timer >= 0.2 then
            self.trail_timer = 0

            local yaw = self.object:get_yaw() or 0
            -- Calculate rear position (behind the entity)
            -- Distance behind entity (adjust based on model size, say 2 nodes behind)
            local back_dist = 2
            local rx = pos.x + math.sin(yaw) * back_dist
            local rz = pos.z - math.cos(yaw) * back_dist
            local rpos = {x = rx, y = pos.y, z = rz}

            minetest.add_particlespawner({
                amount = 1,
                time = 0.1,
                minpos = rpos,
                maxpos = rpos,
                minvel = {x=0, y=0, z=0},
                maxvel = {x=0, y=0, z=0},
                minacc = {x=0, y=0, z=0},
                maxacc = {x=0, y=0, z=0},
                minexptime = 3,
                maxexptime = 6,
                minsize = 1,
                maxsize = 2,
                -- A built-in particle texture or solid white
                texture = "sky_doodles_black.png^[colorize:#FFFFFF:255",
                -- We use the black texture but colorize it to white since we didn't make a white one.
                -- Wait, the prompt says "short-lived, fading white/cloud particle texture".
                -- I'll use a colorized black to make it solid white, or just "default_cloud.png" if it exists,
                -- but we can't assume default depends. Let's just use the white colorized texture.
                glow = 0,
            })
        end

        return false -- let mobs redo continue its other logics (though we overrode movement)
    end,
})
"""

# remove the last "})"
content = content.replace("})", custom_logic)

with open('sky_doodles/init.lua', 'w') as f:
    f.write(content)
