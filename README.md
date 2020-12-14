# SPIS TREŚCI:
* [Wymagane moduły zewnętrzne](#Wymagane-moduły-zewnętrzne)
* [Moduły](#Moduły)
* [Klasy](#Klasy)
	* [enum genetics.SlicingType()](#enum-geneticsslicingtype)
	* [map.Map()](#mapamap)
	* [genetics.Genetics()](#geneticsgenetics)
* [Funkcje](#Funkcje)
	* [genetics.solve()](#geneticssolve)
	* [genetics.print_best_vehicle()](#geneticsprint_best_vehicle)
	* [genetics.plot()](#geneticsplot)
* [Przykłady](#Przykłady)
	* [Przykład 1](#przykład-1)
	* [Przykład 2](#przykład-2)
# Wymagane moduły zewnętrzne:

* NetworkX 2.5
* Matplotlib 3.3.2

```
pip install networkx
pip install matplotlib
```

# Moduły:
Do wyznaczenia rozwiązania problemu potrzebne są 2 moduły:
* map
* genetics

```python
import map
import genetics
```
# Klasy:

## ```enum genetics.SlicingType()```:
Klasa ```genetics.SlicingType()``` jest klasą wyliczeniową (enum) pozwalającą na zmianę sposobu krzyżowania osobników populacji.

Posiada dwie wartości:

```MULTI_POINT_VISITED_EPSILON = 0``` oznacza krzyżowanie wielopunktowe, wycinające fragmenty genomu z otoczenia binarnie reprezentowanej listy odwiedzonych przez pojazd (osobnika) wierzchołków, przykładowo
   
```ONE_POINT_RAND = 1``` oznacza krzyżowanie jednopunktowe z losowo wybranym punktem granicznym genomu.


## ```mapa.Map()```:
Jest to klasa odpoeiwdzialna za reprezentację sieci popłączonych drogami miast, za pomocą grafu ważonego.
Użytkownik może zdefiniować własny obiekt tej klasy, który może zostać poddany analizie za pomoca algorutmu genetycznego.
```python
 mapa.Map(size, edg, as_complete)
```
Jej parametry to:
* ```size``` - odpowiada za liczbę wierzchołków grafu
* ```edg``` (opt) - odpowiada za liczbę krawędzi

UWAGA #1: W przypadku podania zbyt dużej lub zbyt małej wartości względem ilości wierzchołków, nastąpi autokorekta!

* ```as_complete``` (opt) - domyślnie ```False```, dla wartości ```True``` następuje generacja pełnego grafu o zadanym ```size```

## ```genetics.Genetics()```
Jest najważniejszą klasą do funkcjonalności algorytmu i może funkcjonować samodzielnie bez ręcznego tworzenia instancji klasy ```mapa.Map```:
```python
genetics.Genetics(nodes, edges, mapa, vehicles_no, cycles_number, slicing_type)
```
Jej parametry to:
* ```nodes``` - ilość wierzchołków generowanego w sposób losowy grafu ważonego przedstawiającego połączone miasta.
* ```edges``` (opt) - ilość dróg łączących miasta

   UWAGA #1: Domyślne wartości tych dwóch parametrów wynoszą ```0```, a więc wynikowa mapa będzie rozmiaru ```0```
   
* ```mapa``` (opt) - jeśli podano obiekt klasy ```map.Map()``` wartości nodes i edges zostaną zignorowane, nie nastąpi ponowna generacja grafu, ale zostanie wyznaczone rozwiązanie dla zadanego pod tym parametrem grafu
   
   UWAGA #1: Domyślnie parametr ten przyjmuje wartość ```None``` i nie należy go zmieniać jeśli chcemy wygenerować graf o podanym ```nodes``` i ```edges``` dla danej instancji ```genetics.Genetics()```

* ```vehicles_no``` - liczba osobników populacji
* ```cycles_number``` - liczba cykli krzyżowania algorytmu genetycznego
* ```slicing_type``` (opt) - typ krzyżowania, domyślnie wartość ```genetics.SlicingType.MULTI_POINT_VISITED_EPSILON```, lub inaczej ```0```

# Funkcje:
## ```genetics.solve()```:
Funkcja wyznaczająca rozwiązanie problemu, każde jej zawołanie wykona zadaną w konstruktorze obiektu klasy ```genetics.Genetics()``` ilość cykli krzyżowania

## ```genetics.print_best_vehicle()```:
Funkcja wyświetlająca na konsolę parametry najlepszego osobnika (rozwiązania).  Można ją wywołać po zawołaniu funckji  ```genetics.solve()```, w przeciwnym razie zachowanie programu jest nieokreślone.

## ```genetics.plot()```:
Funkcja wyświetlająca wykresy statystyczne wykonania algorytmu. Są to:
* Średnia wieku osobników.
* Ilość ładowarek w rozwiązaniu najlepszego osobnika.
* Przebieg w kilometrach najlepszego osobnika.
* Rozwiązanie w formie grafu o pokolorowanych wierzchołkach, gdzie zielone oznaczają miasto z ładowarką.

# Przykłady:
## Przykład 1:
Przykładowy kod prezentuje sposób rozwiązania problemu, dla losowej, wygenerowanej przez klasę ```genetics.Genetics()``` mapy miast o 20 wierzchołkach, 10 pojazdach (osobnikach), przeprowadzająca 50 cykli, stosująca domyśle krzyżowanie wielopunktowe.
```python
import genetics

gen = genetics.Genetics(nodes=20, vehicles_no=10, cycles_number=50)
gen.solve()
gen.print_best_vehicle()
gen.plot
```
### CONSOLE OUTPUT
```
Progress: 100% [####################################################################################################]

----VEHICLE----
ID:  164
Start:  9
Current node:  7
Battery:  1000  /  1000
Range:  20.0 [km]
Kilometrage:  73 [km]
Battery life:  100 %
---------------
Chargers num:  7
Visited  num:  19
Chrg/Vis rat:  0.3684210526315789
Age:  23
---------------

```
## Przykład 2:
Przykładowy kod badający dwukrotne podejście do rozwiązania problemu dla takiej samej mapy (grafu).
```python
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
```
