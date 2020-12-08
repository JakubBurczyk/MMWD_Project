import map
import vehicle
import genetics

vehicles_number = 50
cycles = 100

mapa = map.Map(100, 0, as_complete=False, tries=10000)
mapa.print()

gen1 = genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles, slicing_type=genetics.SlicingType.VISITED_EPSILON)
gen2 = genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles, slicing_type=genetics.SlicingType.VISITED_EPSILON)

#gen.mapa.print()

# for i in range(200):
#     print("-----------------CYCLE NUMBER ", i + 1, "-----------------")
#     gen.cycle()
#     for v in gen.vehicles:
#         pass
#         #v.print_status()
#     #gen.vehicles[0].print_status();
#
# gen.vehicles[0].print_status()
# gen.plot_avg_age()
# gen.plot_charger_nums_of_best()
# gen.plot_kilometrages_of_best()
# gen.plot_visited_nodes_num_of_best()
# gen.plot_nodes_to_chargers_ratios_of_best()

print("EO MAIN")

