from map_gen import Map

tilemap = Map(2)

while True:
    tilemap.town_spawn()
    tilemap.update_map()
