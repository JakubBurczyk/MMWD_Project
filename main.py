import map
import vehicle
import genetics

vehicles_number = 100
cycles = 200

mapa = map.Map(size=100, as_complete=False, tries=10000)
mapa.print()

gen1 = genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles, slicing_type=genetics.SlicingType.VISITED_EPSILON,show_best=True, show_progress=True, plot_all=True, show_map_solution=False)
# gen2 = genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles, slicing_type=genetics.SlicingType.START_TO_RANDOM,show_best=True, show_progress=True, plot_all=False, show_map_solution=False)



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

