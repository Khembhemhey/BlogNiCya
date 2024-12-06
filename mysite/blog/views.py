from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

# Blog list view with category filtering
@login_required
def blog_list(request):
    category_id = request.GET.get('category')  # Get the category ID from the URL parameters
    if category_id:
        posts = Post.objects.filter(category_id=category_id, author=request.user)  # Filter posts by category and logged-in user
    else:
        posts = Post.objects.filter(author=request.user)  # Filter posts by logged-in user

    categories = Category.objects.all()  # Get all categories for display
    context = {'blog_list': posts, 'categories': categories, 'active_tab': 'blog_list'}
    return render(request, "blog/blog_list.html", context)


@login_required
def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # Fetch all comments for this post

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    context = {
        'blog_detail': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, "blog/blog_detail.html", context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author as the logged-in user
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blog/blog_form.html', {'form': form})


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('dashboard')  # Replace 'dashboard' with your desired redirect URL
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})
@login_required
def dashboard_view(request):
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(category_id=category_id)
    else:
        posts = Post.objects.all()

    categories = Category.objects.all()  # Fetch all categories

    # Pass the data to the template
    context = {
        'posts': posts,
        'categories': categories,
        'active_tab': 'dashboard', 
    }
    return render(request, 'blog/dashboard.html', context)


def comment_view(request):
    # If it's a POST request, save the new comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save the comment and link it to the current user
            comment = form.save(commit=False)
            comment.user = request.user  # Assuming the user is logged in
            comment.save()
            return redirect('comment_view')  # Redirect to the same page after saving
    else:
        form = CommentForm()

    comments = Comment.objects.all()  # Fetch all comments to display
    return render(request, 'comments/comment_view.html', {'form': form, 'comments': comments})

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')  # Order by latest posts
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
