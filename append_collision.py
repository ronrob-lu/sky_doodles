with open('sky_doodles/init.lua', 'r') as f:
    content = f.read()

# We need to insert collision detection and distance despawn into `do_custom`.
# Let's rebuild the do_custom function.

custom_logic = """
    do_custom = function(self, dtime)
        local pos = self.object:get_pos()
        if not pos then return false end

        -- Distance despawn (>100 nodes from nearest player)
        -- We throttle this check to save performance
        self.despawn_timer = (self.despawn_timer or 0) + dtime
        if self.despawn_timer > 2 then
            self.despawn_timer = 0
            local players = minetest.get_connected_players()
            local too_far = true
            for _, player in ipairs(players) do
                local ppos = player:get_pos()
                if ppos and vector.distance(pos, ppos) <= 100 then
                    too_far = false
                    break
                end
            end
            if too_far then
                self.object:remove()
                return false
            end
        end

        -- Enforce Y=136 altitude
        if math.abs(pos.y - 136) > 0.1 then
            pos.y = 136
            self.object:set_pos(pos)
        end

        local yaw = self.object:get_yaw() or 0
        local speed = 4 -- 4 nodes/sec forward speed

        -- Zero out vertical velocity and keep horizontal speed
        local vel = self.object:get_velocity()
        if vel then
            -- Calculate forward velocity based on yaw
            local vx = -math.sin(yaw) * speed
            local vz = math.cos(yaw) * speed
            self.object:set_velocity({x = vx, y = 0, z = vz})
        end

        -- Collision detection
        -- Check for terrain/nodes ~2 nodes ahead
        local front_pos = {
            x = pos.x - math.sin(yaw) * 2,
            y = pos.y,
            z = pos.z + math.cos(yaw) * 2
        }
        -- Check line of sight from pos to front_pos
        local los, blocked_pos = minetest.line_of_sight(pos, front_pos)
        if not los then
            self.object:remove()
            return false
        end

        -- Check for other sky_doodles planes within 3 nodes
        for _, obj in ipairs(minetest.get_objects_inside_radius(pos, 3)) do
            if obj ~= self.object then
                local ent = obj:get_luaentity()
                if ent and ent.name == "sky_doodles:airplane" then
                    -- Destroy both
                    obj:remove()
                    self.object:remove()
                    return false
                end
            end
        end

        -- Cloud trail system
        self.trail_timer = (self.trail_timer or 0) + dtime
        if self.trail_timer >= 0.2 then
            self.trail_timer = 0

            local back_dist = 2
            local rpos = {
                x = pos.x + math.sin(yaw) * back_dist,
                y = pos.y,
                z = pos.z - math.cos(yaw) * back_dist
            }

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
                texture = "sky_doodles_black.png^[colorize:#FFFFFF:255",
                glow = 0,
            })
        end

        return true -- return true to skip Mobs Redo default movement/physics
    end,
})
"""

# Replace the old do_custom
import re
new_content = re.sub(r'    do_custom = function\(self, dtime\).*?\}\)', custom_logic, content, flags=re.DOTALL)

with open('sky_doodles/init.lua', 'w') as f:
    f.write(new_content)
