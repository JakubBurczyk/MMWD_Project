import map
import genetics

vehicles_number = 100
cycles = 100
attempts = 2
tests_number = 3

mapa = map.Map(size=20)
mapa.print()

gen = []
for i in range(attempts):
    gen.append(genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles,slicing_type=genetics.SlicingType.MULTI_POINT_VISITED_EPSILON))

for i in range(attempts):

    gen[i].solve()
    gen[i].print_best_vehicle()
    gen[i].plot()

for i in range(attempts):
    gen[i].test(tests_number)

