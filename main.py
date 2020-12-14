import map
import genetics

vehicles_number = 100
cycles = 100
attempts = 2

mapa = map.Map(size=100)
mapa.print()

gen = [genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles, slicing_type=genetics.SlicingType.MULTI_POINT_VISITED_EPSILON)] * attempts

for i in range(attempts):
    gen[i].solve()
    gen[i].print_best_vehicle()
    gen[i].plot()


