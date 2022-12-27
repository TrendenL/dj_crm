from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from leads.views import landing_page, LandingPageView, SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login" ),
    path("logout/", LogoutView.as_view(), name="logout" ),
    path("signup/", SignupView.as_view(), name="signup" ),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("leads/", include("leads.urls", namespace="leads")),
    path("agents/", include("agents.urls", namespace="agents")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
