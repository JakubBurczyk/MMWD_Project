import map
import vehicle

m1 = map.Map(20, as_complete=True)
m1.print()
print(m1.get_distance_between(0, 1))
print("Chargers:")
print(m1.count_chargers())

v1 = vehicle.Vehicle(m1)
v2 = vehicle.Vehicle(m1)

v1.print_occupied_IDs()


v1.print_status()
v2.print_status()

#m1.print()