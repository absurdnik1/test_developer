from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point, Polygon
from .models import DumpTruck, Storage, Location


tipper_101 = DumpTruck('101', 'Belaz', 120, 100, 32, 65)
tipper_102 = DumpTruck('103', 'Belaz', 120, 125, 30, 65) 
tipper_103 = DumpTruck('K103', 'Komatsu', 110, 120, 35, 62)

storage = Storage('Central', 900, 34, 65, polygon=Polygon(((30, 10), (40, 40),
                                                           (20, 40), (10, 20),
                                                           (30, 10))))


def index(request):
    template = 'index.html'
    dump_trucks = DumpTruck.objects.all()
    storage = Storage.objects.first()

    if request.method == 'POST':
        x, y = [float(coord) for coord in request.POST['coordinates'].split()]
        point = Point(x, y, srid=4326)
    
        if storage.polygon.contains(point):
            for truck in dump_trucks:
                storage.current_weight += truck.current_weight
                storage.SiO2 = ((storage.current_weight * storage.SiO2 +
                                truck.current_weight * truck.SiO2) /
                                storage.current_weight)
                storage.FE = ((storage.current_weight * storage.FE +
                              truck.current_weight * truck.FE) /
                              storage.current_weight) 
            storage.save()

            for truck in dump_trucks:
                Location.objects.create(
                    dump_track=truck,
                    location=point
                )
    
        return redirect('/')

    context = {
        'dump_trucks': dump_trucks,
        'storage': storage,
    }

    return render(request, template, context)
    
