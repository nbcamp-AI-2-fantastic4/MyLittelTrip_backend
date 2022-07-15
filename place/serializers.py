from rest_framework import serializers


from place.models import Place,PlaceType
from user.models import User

class PlaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceType
        fields = ['id','typename']
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class PlaceSerializer(serializers.ModelSerializer):
    user = Userserializer(read_only=True)
    typename = PlaceTypeSerializer(read_only=True)
    # def get_user(self, obj):
    #     return obj.user.username

    # def get_typename(self,obj):
    #     return obj.PlaceType.typename

    def create(self, validated_data):
        place = Place(**validated_data)
        place.save()
        return place

    class Meta:
        model = Place
        fields = [
            'id',
            'user',
            'typename',
            'name',
            'word',
            'address',
            'x',
            'y',
            'image',
            'rating',
            'description'
        ]