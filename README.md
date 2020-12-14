# SPIS TREŚCI:
* [Wymagane moduły zewnętrzne](#Wymagane-moduły-zewnętrzne)
* [Moduły](#Moduły)
* [Klasy](#Klasy)
* [a](## ```enum-genetics.SlicingType()```)

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
Klasa genetics.SlicingType jest klasą wyliczeniową (enum) pozwalającą na zmianę sposobu krzyżowania osobników populacji.

Posiada dwie wartości:

```MULTI_POINT_VISITED_EPSILON = 0``` oznacza krzyżowanie wielopunktowe, wycinające fragmenty genomu z otoczenia binarnie reprezentowanej listy odwiedzonych przez pojazd (osobnika) wierzchołków, przykładowo
   
```ONE_POINT_RAND = 1``` oznacza krzyżowanie jednopunktowe z losowo wybranym punktem granicznym genomuL


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
   
* ```mapa``` (opt) - jeśli podano obiekt klasy ```map.MAP()``` wartości nodes i edges zostaną zignorowane, nie nastąpi ponowna generacja grafu, ale zostanie wyznaczone rozwiązanie dla zadanego pod tym parametrem grafu
   
   UWAGA #1: Domyślnie parametr ten przyjmuje wartość ```None``` i nie należy go zmieniać jeśli chcemy wygenerować graf o podanym ```nodes``` i ```edges``` dla danej instancji ```genetics.Genetics()```

