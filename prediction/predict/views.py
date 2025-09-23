from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .ml_model import predict_price as predict_price_fn


def predict_price(request):
	prediction = None
	error = None
	# form values
	size_val = request.POST.get("size") if request.method == "POST" else ""
	bedrooms_val = request.POST.get("bedrooms") if request.method == "POST" else ""
	age_val = request.POST.get("age") if request.method == "POST" else ""
	location_val = request.POST.get("location") if request.method == "POST" else "Downtown"
	house_type_val = request.POST.get("house_type") if request.method == "POST" else "Villa"

	if request.method == "POST":
		try:
			# validation and casting
			if size_val in (None, "") or bedrooms_val in (None, "") or age_val in (None, ""):
				raise ValueError("All fields are required.")

			size = float(size_val)
			bedrooms = int(bedrooms_val)
			age = int(age_val)

			prediction = predict_price_fn(
				size=size,
				bedrooms=bedrooms,
				age=age,
				location=location_val,
				house_type=house_type_val,
			)
		except Exception as exc:
			error = str(exc)

	context = {
		"prediction": prediction,
		"error": error,
		"form": {
			"size": size_val,
			"bedrooms": bedrooms_val,
			"age": age_val,
			"location": location_val,
			"house_type": house_type_val,
		},
		"locations": ["Downtown", "Suburbs", "Rural"],
		"house_types": ["Villa", "Apartment", "L-shape", "Normal"],
	}
	return render(request, "predict.html", context)
