from rest_framework import serializers

from .models import User as UserModel

class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email"]

        extra_kwargs = {
            'password': {'write_only': True}
        }

   def create(self, validated_data):
      password = validated_data.pop('password')
      user = UserModel.objects.create(**validated_data)
      user.set_password(password)
      user.save()

      return user   

   def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save()
        return instance