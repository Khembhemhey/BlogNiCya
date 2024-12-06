from rest_framework import serializers
from .models import Category, Post, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display username instead of ID
    comments = CommentSerializer(many=True, read_only=True)  # Include related comments
    category_name = serializers.CharField(source='category.name', read_only=True)  # Include category name

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'image', 'category', 'category_name', 
            'created_at', 'updated_at', 'author', 'comments'
        ]
