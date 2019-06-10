from map_gen import Map

tilemap = Map(5)
tilemap.town_spawn()

while True:
    tilemap.update_map()
