from rest_framework import serializers
from django.db.models.query_utils import Q

from .models import Review, ReviewImage
from comment.models import Like

from trip.serializers import TripSerializer


# 이미지 모델 시리얼라이저
class ReviewImageSerializer(serializers.ModelSerializer):
    order = serializers.ReadOnlyField()
    class Meta:
        model = ReviewImage
        fields = ['review_id', 'order', 'image']


# 리뷰 조회, 작성 시리얼라이저
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    # images = ReviewImageSerializer(source='reviewimage_set')
    likes = serializers.SerializerMethodField()

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
        likes_objs = Like.objects.filter(query)
        
        likes_count = likes_objs.count()
        return likes_count

    class Meta:
        model = Review
        fields = ['user', 'title', 'content', 
                  'created_at', 'images', 'likes']


# 리뷰 상세조회 시리얼라이저
class ReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    trip = TripSerializer()
    likes = serializers.SerializerMethodField()


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

    def get_likes(self, obj):
        query = (
            Q(posttype_id = 1) & 
            Q(post_id = obj.id)
        )
        likes_objs = Like.objects.filter(query)
 
        likes_count = likes_objs.count()
        return likes_count

    class Meta:
        model = Review
        fields = ['user', 'created_at', 'trip', 'title', 
                  'content', 'images', 'likes']