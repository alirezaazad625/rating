from typing import Optional

from django.db import transaction
from limits import RateLimitItemPerMinute
from limits.storage import MemoryStorage
from limits.strategies import FixedWindowRateLimiter
from rest_framework import views, status, generics
from rest_framework.response import Response

from .models import Rating, PostRating, RatingStatus
from .serializers import UpsertRatingSerializer

rate_limit = RateLimitItemPerMinute(100)
storage = MemoryStorage()
limiter = FixedWindowRateLimiter(storage)


class RatingOverview(views.APIView):
    def get(self, request, post_id: int, *args, **kwargs):
        post_rating = PostRating.objects.filter(post_id=post_id).get()
        return Response(
            {
                "rates_count": post_rating.count,
                "rates_mean": round(post_rating.sum / post_rating.count, 1)
            },
            status=status.HTTP_200_OK)


class RatingUpsert(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UpsertRatingSerializer(data=request.data)
        if serializer.is_valid():
            rating: Rating = Rating.objects.filter(
                user_id=request.get("user_id"),
                post_id=request.get("post_id")
            ).first()
            if limiter.hit(rate_limit):
                request = serializer.validated_data
                previous_rating = None
                if rating:
                    previous_rating = rating.value
                else:
                    rating = Rating(
                        user_id=request.get("user_id"),
                        post_id=request.get("post_id"),
                    )
                rating.value = request.get("value")
                rating.status = RatingStatus.APPROVED
                update_rating(rating=rating, previous_rating=previous_rating)
            else:
                rating = Rating(
                    user_id=request.get("user_id"),
                    post_id=request.get("post_id"),
                    status=RatingStatus.PENDING,
                    value=request.get("value"),
                )
                rating.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingApprove(views.APIView):
    def post(self, request, post_id, user_id, *args, **kwargs):
        rating: Rating = Rating.objects.filter(
            user_id=user_id,
            post_id=post_id
        ).get()
        rating.status = RatingStatus.APPROVED
        update_rating(rating=rating)


class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.first(status=RatingStatus.APPROVED).all()
    serializer_class = UpsertRatingSerializer


@transaction.atomic
def update_rating(rating: Rating, previous_rating: Optional[int] = None) -> None:
    post_rating: PostRating = PostRating.objects.filter(post_id=rating.post_id).first()
    if post_rating:
        post_rating.sum += rating.value
        if previous_rating:
            post_rating.sum -= previous_rating
        else:
            post_rating.count += 1
    else:
        post_rating = PostRating(post_id=rating.post_id, sum=rating.value, count=1)
    rating.save()
    post_rating.save()
