from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform


class WatchListSerializer(serializers.ModelSerializer):
    len_of_title = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        fields = '__all__'
        # fields = ['id', 'title', 'description']
        # exclude = ['active'] # fields or exclude - not possible use both

    def get_len_of_title(self, object):  # get_ a potem nazwa pola- tutaj tworzymy wartosć dla SerializerMethodField()
        return len(object.title)
    #
    # ##Vaidators must be addded as functions
    # def validate_title(self, value):  # musi zaczynać się od validate_ a potem pole
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is to short!")
    #     else:
    #         return value
    #
    # def validate(self, data):  # cały klasa
    #     if data['title'] == data['description']:
    #         raise serializers.ValidationError("Title and description can't be the same")
    #     return data


#
# def title_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Title is too short')
#     return value
#
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(validators=[title_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

# def validate_title(self, value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is to short!")
#     else:
#         return value

# def validate(self, data):
#     if data['title'] == data['description']:
#         raise serializers.ValidationError("Title and description can't be the same")
#     return data


class StreamPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = '__all__'
