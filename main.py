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

gen = genetics.Genetics(nodes=100, edges=0, vehicles_no=200)
# print(gen.mapa.neighbours(2))

gen.mapa.print()

for i in range(1000):
    print("-----------------CYCLE NUMBER ", i + 1, "-----------------")
    gen.cycle()
    for v in gen.vehicles:
        pass
        #v.print_status()
    #gen.vehicles[0].print_status();

gen.vehicles[0].print_status()
gen.plot_avg_age()
gen.plot_charger_nums_of_best()
gen.plot_kilometrages_of_best()
gen.plot_visited_nodes_num_of_best()
gen.plot_nodes_to_chargers_ratios_of_best()

print("EO MAIN")
m1.print()
