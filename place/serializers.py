from rest_framework import serializers


from place.models import Place, PlaceType
from user.models import User
from user.serializers import UserSerializer

class PlaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceType
        fields = ['id', 'typename']





class PlaceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    placetype = serializers.SerializerMethodField(read_only=True)
     
    def get_user(self, obj):
         return obj.user.username


    def get_placetype(self,obj):
        return obj.placetype.typename

    # def create(self, validated_data):
    #     place = Place(**validated_data)
    #     place.save()
    #     return place

    class Meta:
        model = Place
        fields = [
            'id',
            'user',
            'placetype',
            'name',
            'word',
            'address',
            'x',
            'y',
            'image',
            'rating',
            'description'
        ]


class PlaceAddSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    placetype = PlaceTypeSerializer()

    def validate(self, data):
        print(data)
        return data

    def create(self, validated_data):
        place = Place(**validated_data)
        # place.save()
        return place

    def get_placetype(self, obj):
        placetype_obj = obj.reviewimage_set.all()
        placetype_data = {
            'placetype_id': placetype_obj.placetype_id,
            'placetype_typename': placetype_obj.placetype_typename,
        }
        return placetype_data

    class Meta:
        model = Place
        fields = [
            'id',
            'user',
            'placetype',
            'name',
            'address',
            'x',
            'y',
            'image',
            'description'
        ]
