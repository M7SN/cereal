from main.models import Manufacturer

def main_menu(request):

	manus = Manufacturer.objects.all()

	return { 'main_menu' : manus }