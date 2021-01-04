import map
import genetics
import time
import matplotlib.pyplot as plt
from statistics import mean

vehicles_number = 100
cycles = 200
attempts = 1
tests_number = 1

mapa = map.Map(size=100)
mapa.print(vehicles_number=100, cycles=200)

gen_vis_chargers_ratio = []
gen_vis_size_ratio = []
gen_chargers_size_ratio = []
gen_time = []
gen_try = []
gen = []

for i in range(attempts):
    gen.append(genetics.Genetics(mapa=mapa, vehicles_no=vehicles_number, cycles_number=cycles,
                                 slicing_type=genetics.SlicingType.MULTI_POINT_VISITED_EPSILON))

for i in range(attempts):
    print("ATTEMPT: ", i + 1)
    gen_try.append(i)

    start = time.time()
    gen[i].solve()
    gen_time.append(time.time() - start)

    gen_chargers_size_ratio.append(gen[i].get_chargers_to_size_ratio())
    gen_vis_size_ratio.append(gen[i].get_vis_to_size_ratio())
    gen_vis_chargers_ratio.append(gen[i].best_vehicle.get_ratio())
    gen[i].print_best_vehicle()
    # gen[i].plot()

plt.scatter(gen_try, gen_vis_chargers_ratio)
plt.xticks(gen_try)
plt.title("Stosunek ładowarki/odwiedzone wierzchołki\nw poszczególnych próbach, średnia: " +
          str(round(mean(gen_vis_chargers_ratio), 2)))
plt.xlabel("Próba")
plt.show()

plt.scatter(gen_try, gen_vis_size_ratio)
plt.xticks(gen_try)
plt.title("Stosunek odwiedzone wierzchołki/rozmiar mapy\nw poszczególnych próbach, średnia: " +
          str(round(mean(gen_vis_size_ratio), 2)))
plt.xlabel("Próba")
plt.show()

plt.scatter(gen_try, gen_chargers_size_ratio)
plt.xticks(gen_try)
plt.title("Stosunek ilość ładowarek/rozmiar mapy w\n poszczególnych próbach, średnia: " +
          str(round(mean(gen_chargers_size_ratio), 2)))
plt.xlabel("Próba")
plt.show()

plt.scatter(gen_try, gen_time)
plt.xticks(gen_try)
plt.title("Czasy wykonania prób\nśrednia: " +
          str(round(mean(gen_time), 2)))
plt.ylabel("Czas [s]")
plt.xlabel("Próba")
plt.show()

# for i in range(attempts):
#     gen[i].test(tests_number)
