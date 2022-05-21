from rest_framework import serializers

from .models import Comment, Movie


class MovieQuerySerializer(serializers.Serializer):
    title = serializers.CharField()
    release_year = serializers.IntegerField(min_value=1950, max_value=2050)


class MovieSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class MovieSerializerIn(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ["id"]


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "year", "genre", "director"]


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["movie", "text"]


class CommentCreateOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "movie", "text"]
