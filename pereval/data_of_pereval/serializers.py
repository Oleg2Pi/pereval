from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'surname', 'name', 'otc', 'phone', ]


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalCoordinate
        fields = ['latitude', 'longitude', 'height', ]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalLevel
        fields = ['winter', 'summer', 'autumn', 'spring', ]


class ImageSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = ImageModel
        fields = ['title', 'data', ]


class PerevalSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)
    user = UserSerializer()
    coord = CoordinateSerializer()
    level = LevelSerializer(allow_null=True, default=False)
    images = ImageSerializer(many=True)

    class Meta:

        model = PerevalModel
        fields = [
            'id', 'status', 'beauty_title', 'title', 'other_title', 'connect',
            'add_time', 'user', 'coord', 'level', 'images',
        ]

    def create(self, validated_data, **kwargs):

        user = validated_data.pop('user')
        coord = validated_data.pop('coord')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = UserModel.objects.get_or_create(**user)

        coord = PerevalCoordinate.objects.create(**coord)
        level = PerevalLevel.objects.create(**level)
        pereval = PerevalModel.objects.create(**validated_data, user=user, level=level, coord=coord)

        for img in images:
            title = img.pop('title')
            data = img.pop('data')
            ImageModel.objects.create(title=title, data=data, pereval=pereval)

        return pereval

    def validate(self, value):

        user_data = value['user']

        if self.instance:
            if (user_data['email'] != self.instance.user.email
                    or user_data['surname'] != self.instance.user.surname
                    or user_data['name'] != self.instance.user.name
                    or user_data['otc'] != self.instance.user.otc
                    or user_data['phone'] != self.instance.user.phone):

                raise serializers.ValidationError()

        return value


class PerevalListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    user = UserSerializer()
    coord = CoordinateSerializer()
    level = LevelSerializer()

    class Meta:
        model = PerevalModel
        fields = [
            'id', 'status', 'beauty_title', 'title', 'other_title', 'connect',
            'add_time', 'user', 'coord', 'level', 'images'
        ]