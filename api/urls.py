from django.urls import path, re_path
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from api.views import blog
from .views import casting, service, user, email
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Galharufa API",
        default_version='v1',
        description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        #license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),

    path('users', user.GetUserView.as_view(), name='users'),
    path('user/register', user.RegistrationView.as_view(), name='register'),
    path('user/login', user.LoginView.as_view(), name='login'),
    path('user/logout', user.LogoutView.as_view(), name='logout'),
    path('user/change-password',
         user.ChangePasswordView.as_view(), name='change-password'),
    path('user/deactivate-account',
         user.DeactivateUserView.as_view(), name='deactivate-account'),
    path('user/reactivate-account',
         user.ReactivateUserView.as_view(), name='reactivate-account'),

    path('upload-images', casting.FotosView.as_view(), name='upload-images'),
    path('casting', casting.CastingsView.as_view(), name='castings'),
    path('casting/<slug:slug>', casting.CastingView.as_view(), name='casting'),

    path('service',
         service.ServicosView.as_view(), name='services'),
    path('service/<slug:slug>',
         service.ServicoView.as_view(), name='service'),

    path('blog', blog.BlogPostsView.as_view(), name='blog-posts'),
    path('blog/<slug:slug>', blog.BlogPostView.as_view(), name='blog-post'),

    path('email', email.EmailSenderView.as_view(), name='send-email'),
    path('csrf_token', email.csrf_token, name='csrf_token'),

    path('token-refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
