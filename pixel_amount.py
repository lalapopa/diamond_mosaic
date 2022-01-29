def cm_to_pixel(w, h):
	dpi = 300
	return (round((w/2.54)*dpi), round((h/2.54)*dpi))
print(cm_to_pixel(0.25, 0.25))