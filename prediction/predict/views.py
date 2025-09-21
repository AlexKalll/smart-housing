from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .ml_model import HousePricePredictor


def predict_price(request):
	prediction = None
	error = None

	# Keep entered values to repopulate the form on error
	size_val = request.POST.get("size") if request.method == "POST" else ""
	bedrooms_val = request.POST.get("bedrooms") if request.method == "POST" else ""
	age_val = request.POST.get("age") if request.method == "POST" else ""

	if request.method == "POST":
		try:
			# Basic validation and casting
			if size_val in (None, "") or bedrooms_val in (None, "") or age_val in (None, ""):
				raise ValueError("All fields are required.")

			size = float(size_val)
			bedrooms = int(bedrooms_val)
			age = float(age_val)

			predictor = HousePricePredictor()
			prediction = predictor.predict(size=size, bedrooms=bedrooms, age=age)
		except Exception as exc:
			# Keep it simple for now; surface the error message
			error = str(exc)

	context = {
		"prediction": prediction,
		"error": error,
		"form": {"size": size_val, "bedrooms": bedrooms_val, "age": age_val},
	}
	return render(request, "predict.html", context)
