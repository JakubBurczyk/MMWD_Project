# SPIS TREŚCI:
* [Wymagane moduły](https://github.com/JakubBurczyk/MMWD_Project/blob/master/README.md#wymagane-modu%C5%82y)
* [Instrukcja obsługi](https://github.com/JakubBurczyk/MMWD_Project/blob/master/README.md#instrukcja-obs%C5%82ugi)
   * [Moduły]()
   * []()
# Wymagane moduły:

* NetworkX 2.5
* Matplotlib 3.3.2

```
pip install networkx
pip install matplotlib
```

# INSTRUKCJA OBSŁUGI:

## Moduły:
Do wyznaczenia rozwiązania problemu potrzebne są 2 moduły:
* map
* genetics

```python
import map
import genetics
```
## Klasy:
### ```enum genetics.SlicingType```:
Klasa genetics.SlicingType jest klasą wyliczeniową (enum) pozwalającą na zmianę sposobu krzyżowania osobników populacji.

Posiada dwie wartości:

```MULTI_POINT_VISITED_EPSILON``` o liczbowej wartości ```0```
```ONE_POINT_RAND``` o liczbowej wartości ```1```

```MULTI_POINT_VISITED_EPSILON``` oznacza krzyżowanie wielopunktowe, wycinające fragmenty genomu z otoczenia binarnie reprezentowanej listy odwiedzonych przez pojazd (osobnika) wierzchołków, przykładowo
   
```ONE_POINT_RAND``` oznacza krzyżowanie jednopunktowe z losowo wybranym punktem granicznym genomuL


Najważniejszą klasą, jest ```genetics.Genetics()```, która może funkcjonować samodzielnie:
```python
genetics.Genetics(nodes, edges, mapa, vehicles_no, cycles_number, slicing_type)
```
Jej parametry to:
* ```nodes``` - ilość wierzchołków generowanego w sposób losowy grafu ważonego przedstawiającego połączone miasta.
* ```edges``` - ilość dróg łączących miasta

   UWAGA #1: W przypadku podania zbyt dużej lub zbyt małej wartości względem ilości wierzchołków, nastąpi autokorekta!
   
   UWAGA #2: Domyślne wartości tych dwóch parametrów wynoszą 0
   
* ```mapa``` - jeśli podano obiekt klasy ```map.MAP()``` wartości nodes i edges zostaną zignorowane, nie nastąpi ponowna generacja grafu, ale zostanie wyznaczone rozwiązanie dla zadanego pod tym parametrem grafu
   
   UWAGA #1: Domyślnie parametr ten przyjmuje wartość ```None``` i nie należy go zmieniać jeśli chcemy wygenerować graf o podanym ```nodes``` i ```edges``` dla danej instancji ```genetics.Genetics()```

