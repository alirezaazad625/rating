"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import RatingUpsert, RatingListView, RatingOverview, RatingApprove

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rating/create/', RatingUpsert.as_view(), name='rating-upsert'),
    path('api/rating/approve/<int:post_id>/<int:user_id>', RatingApprove.as_view(), name='rating-approve'),
    path('api/post/overview/<int:post_id>', RatingOverview.as_view(), name='post-overview'),
    path('api/rating/', RatingListView.as_view(), name='rating-list')
]
