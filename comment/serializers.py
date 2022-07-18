from rest_framework import serializers

from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    posttype = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_posttype(self, obj):
        return obj.posttype.typename

    class Meta:
        model = Comment
        fields = ["id", "username", "posttype", "comment", "rating", "post_id"]
        # read_only_fields = ["user", ]
        extra_kwargs = {
            "post_id": {"write_only": True}
        }

    def validate(self, data):
        print(data)
        return data

    # def create(self, validated_data) : 
    #     print(validated_data)
    #     return Comment()
