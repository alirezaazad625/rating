from rest_framework import serializers

from .models import Rating, PostRating


class UpsertRatingSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()
    value = serializers.IntegerField(min_value=1, max_value=5)
    user_id = serializers.IntegerField()

    class Meta:
        model = Rating
        fields = '__all__'

