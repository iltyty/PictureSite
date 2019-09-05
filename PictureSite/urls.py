from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
	path('', RedirectView.as_view(url='/pictures'), name='home'),
	path('accounts/', include('signup.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('admin/', admin.site.urls),
	path('pictures/', include('pictures.urls')),
]
