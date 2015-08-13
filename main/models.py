from django.db import models

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.name

class Cereal(models.Model):
    name = models.CharField(max_length=40, null=True)
    manufacturer = models.ForeignKey('main.Manufacturer', null=True)
    type = models.CharField(max_length=40, null=True, blank=True)
    display_shelf = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="cereal", null=True)
    info = models.TextField()


    def __unicode__(self):
        return self.name

class Nutrition(models.Model):
    calories = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)
    sodium = models.FloatField(null=True)
    dietary_fiber = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    sugars = models.IntegerField(null=True)
    potassium = models.IntegerField(null=True)
    vitamins_and_minerals = models.IntegerField(null=True)
    serving_size_weight = models.FloatField(null=True)
    cups_per_serving = models.FloatField(null=True)
    cereal = models.OneToOneField('main.Cereal', null=True)

    def __unicode__(self):
        return self.cereal.name

    def nutrition_list(self):
        value_list = []
        value_list.append("Protien: %s" % self.protein)
        value_list.append("Calories: %s" % self.calories)
        value_list.append("Fat: %s" % self.fat)
        value_list.append("Sodium: %s" % self.sodium)
        value_list.append("Fiber: %s" % self.dietary_fiber)
        value_list.append("Carbs: %s" % self.carbs)
        value_list.append("Sugar: %s" % self.sugars)
        value_list.append("Potassium: %s" % self.potassium)
        value_list.append("Vitamins & Minerals: %s" % self.vitamins_and_minerals)

        return value_list