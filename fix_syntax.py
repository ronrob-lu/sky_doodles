# Fix the error in the clearance check logic where `self.object` is referenced but `self` is just the object from mobs API depending on the Mobs Redo version.
# Actually, the on_spawn parameter for `mobs:spawn` receives `(self, pos)` where self is the entity.
# Wait, looking at mobs redo API, on_spawn gets `(self, pos)`. But if we remove it immediately, it's better to just return false.
# Returning false might not stop the spawn if mobs redo ignores return value.
# Actually we can do self.object:remove() if the parameter is `self`.

# Wait, `mobs:register_spawn` is the documented function name in the prompt. "Use `mobs:register_spawn` OR a global ABM/globalstep spawner". Let's change `mobs:spawn` to `mobs:register_spawn` just to be safe, using the modern syntax or old syntax.
# Modern mobs redo uses `mobs:spawn` or `mobs:register_spawn`. Both are typically aliased. Let's stick with `mobs:register_spawn`.
