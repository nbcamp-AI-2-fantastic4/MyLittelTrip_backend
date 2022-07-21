from rest_framework import serializers

from comment.models import Like

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    posttype = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_posttype(self, obj):
        return obj.posttype.typename

    class Meta:
        model = Like
        fields = ["user", "posttype", "post_id"]
        