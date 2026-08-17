-- Sky Doodles Mod
-- Autonomous, non-interactive decorative airplanes

minetest.register_entity("sky_doodles:airplane", {
    initial_properties = {
        hp_max = 1,
        physical = true,
        collide_with_objects = true,
        collisionbox = {-6, -3, -6, 6, 3, 6},
        visual = "mesh",
        mesh = "airliner.obj",
        textures = {"sky_doodles_black.png"},
        visual_size = {x = 3, y = 3, z = 3},
        makes_footstep_sound = false,
        static_save = false, -- decorative, no need to save to disk
    },

    on_activate = function(self, staticdata, dtime_s)
        self.object:set_armor_groups({immortal = 1})
        local yaw = math.random() * math.pi * 2
        self.object:set_yaw(yaw)
        local speed = 4
        self.object:set_velocity({
            x = -math.sin(yaw) * speed,
            y = 0,
            z = math.cos(yaw) * speed
        })
    end,

    on_punch = function(self, puncher, time_from_last_punch, tool_capabilities, dir)
        return false -- No interaction
    end,
    on_rightclick = function(self, clicker)
        return false -- No interaction
    end,

    on_step = function(self, dtime)
        local pos = self.object:get_pos()
        if not pos then return end

        -- Distance despawn (>500 nodes from nearest player)
        self.despawn_timer = (self.despawn_timer or 0) + dtime
        if self.despawn_timer > 2 then
            self.despawn_timer = 0
            local players = minetest.get_connected_players()
            local too_far = true
            for _, player in ipairs(players) do
                local ppos = player:get_pos()
                if ppos and vector.distance(pos, ppos) <= 500 then
                    too_far = false
                    break
                end
            end
            if too_far then
                self.object:remove()
                return
            end
        end

        -- Enforce Y=200 altitude
        if math.abs(pos.y - 200) > 0.1 then
            pos.y = 200
            self.object:set_pos(pos)
        end

        local yaw = self.object:get_yaw() or 0
        local speed = 4 -- 4 nodes/sec forward speed

        -- Zero out vertical velocity and keep horizontal speed
        local vel = self.object:get_velocity()
        if vel then
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
            return
        end

        -- Check for other sky_doodles planes within 3 nodes
        for _, obj in ipairs(minetest.get_objects_inside_radius(pos, 3)) do
            if obj ~= self.object then
                local ent = obj:get_luaentity()
                if ent and ent.name == "sky_doodles:airplane" then
                    -- Destroy both
                    obj:remove()
                    self.object:remove()
                    return
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
    end,
})

-- Custom ABM spawner for airplanes
minetest.register_abm({
    label = "sky_doodles_spawner",
    nodenames = {"air"},
    interval = 10,
    chance = 50, -- 1 in 50 chance every 10 seconds per air node (quite low since air is everywhere)
    min_y = 200,
    max_y = 200,
    action = function(pos, node, active_object_count, active_object_count_wider)
        if active_object_count_wider > 2 then
            return -- Limit number of planes nearby
        end

        -- Check light level (only spawn during day/light conditions)
        local light = minetest.get_node_light(pos)
        if not light then
            return
        end

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
            local n = minetest.get_node(p)
            if n and n.name ~= "air" and n.name ~= "ignore" then
                -- Clearance check failed
                return
            end
        end

        minetest.add_entity(pos, "sky_doodles:airplane")
    end,
})
