#!/usr/bin/env python
import csv, os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from main.models import Manufacturer, Cereal, Nutrition

csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cereal.csv")

csv_file = open(csv_file_path, 'r')

reader = csv.DictReader(csv_file)

for row in reader:
    manu_obj = Manufacturer()
    manu_obj, created = Manufacturer.objects.get_or_create(name=row['Manufacturer'])

    print manu_obj.name
    print created

    manu_obj.save()

    cereal_obj, created = Cereal.objects.get_or_create(name=row['Cereal Name'].replace('_',' '))
    cereal_obj.manufacturer = manu_obj
    cereal_obj.save()

    nutri_obj = Nutrition()
    nutri_obj, created = Nutrition.objects.get_or_create(calories=row['Calories'],
                                                         protein=row['Protein (g)'],
                                                         fat=row['Fat'],
                                                         sodium=row['Sodium'], 
                                                         dietary_fiber=row['Dietary Fiber'],
                                                         carbs=row['Carbs'],
                                                         sugars=row['Sugars'],
                                                         potassium=row['Potassium'], 
                                                         vitamins_and_minerals=row['Vitamins and Minerals'], 
                                                         serving_size_weight=row['Serving Size Weight'],
                                                         cups_per_serving=row['Cups per Serving'],
                                                         cereal=cereal_obj,)

    nutri_obj.save()
