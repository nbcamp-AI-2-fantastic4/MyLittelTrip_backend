from rest_framework import serializers
from django.db.models.query_utils import Q

from .models import Review, ReviewImage

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'order', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    # images = ReviewImageSerializer(source='reviewimage_set')
    likes = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return obj.user.username

    def get_images(self, obj):
        image_obj = obj.reviewimage_set.all().first()
        image_data = {
            'review_id' : image_obj.review_id, 
            'order' : image_obj.order, 
            'image' : str(image_obj.image)
            }
        
        return image_data

    def get_likes(self, obj):
        query = (
            Q(posttype_id = 1) & 
            Q(post_id = obj.id)
        )
        likes_objs = obj.user.like_set.filter(query)
 
        likes_count = likes_objs.count()
        return likes_count

    class Meta:
        model = Review
        fields = ['user', 'title', 'content', 'created_at', 'images', 'likes']


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_images(self, obj):

        image_list = []

        for i in obj.reviewimage_set.all():
            image_data = {
                "review_id" : i.review_id,
                "order" : i.order,
                "image" : str(i.image)
            }
            image_list.append(image_data)
        
        return image_list

    class Meta:
        model = Review
        fields = ['user', 'created_at', 'trip', 'title', 'content', 'images']