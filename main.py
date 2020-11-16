import map
import vehicle
import genetics

# m1 = map.Map(20, as_complete=False,tries=100)
# m1.print()
# print(m1.get_distance_between(0, 1))
# print("Chargers:")
# print(m1.count_chargers())
#
# v1 = vehicle.Vehicle(m1)
# v2 = vehicle.Vehicle(m1)
#
# v1.print_occupied_IDs()
#
#
# v1.print_status()
# v2.print_status()

gen = genetics.Genetics(nodes = 20, edges = 0, vehicles_no=5)
print(gen.mapa.neighbours(2))
#gen.mapa.print()

gen.cycle()
for v in gen.vehicles:
    v.print_status()
# m1.print()
