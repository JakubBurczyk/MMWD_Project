# Wymagane moduły:

* NetworkX 2.5
* Matplotlib 3.3.2

```
pip install networkx
pip install matplotlib
```

# INSTRUKCJA OBSŁUGI:

Do wyznaczenia rozwiązania problemu potrzebne są 2 moduły:
* map
* genetics

```python
import map
import genetics
```

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

