import map
import vehicle


class Genetics:
    def __init__(self, mapsize: int = 0, mapedges: int = 0, vehiclesno: int = 100):
        self.Mapa = map.Map(mapsize, mapedges, as_complete=False, tries=100)
        self.Vehicles = []
        for i in range(vehiclesno):
            self.Vehicles.append(vehicle.Vehicle(self.Mapa))
