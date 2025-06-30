from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import PetUserCreationForm, PetUserLoginForm, PostCreationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, PetUser, Like, Comment, Subscription
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
@require_POST
def add_comment(request, post_id):
    try:
        if request.content_type != 'application/json':
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid content type'
            }, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)

        text = data.get('text', '').strip()

        if not text:
            return JsonResponse({
                'status': 'error',
                'message': 'Пустой комментарий'
            }, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Не авторизован'
            }, status=403)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Пост не найден'
            }, status=404)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            text=text
        )

        author_name = (
            request.user.pet_name
            if getattr(request.user, 'pet_name', None)
            else request.user.username
        )

        if not author_name:
            author_name = "Аноним"

        return JsonResponse({
            'status': 'ok',
            'author_name': author_name,
            'text': text,
            'comments_count': post.comments.count()
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_POST
def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()

    return JsonResponse({
        'status': 'ok',
        'is_liked': created,
        'likes_count': post.likes.count()
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('my_profile')
    else:
        form = PostCreationForm()
    return render(request, 'core/create_post.html', {'form': form})


def feed(request):
    posts = Post.objects.all().select_related('author')
    return render(request, 'core/feed.html', {'posts': posts})


def profile(request, user_id):
    user = get_object_or_404(PetUser, id=user_id)
    subscription_exists = False

    if request.user.is_authenticated:
        subscription_exists = Subscription.objects.filter(
            subscriber=request.user,
            target=user
        ).exists()

    return render(request, 'core/profile.html', {
        'profile_user': user,
        'posts': user.posts.all(),
        'is_owner': request.user == user,
        'subscription_exists': subscription_exists
    })

@login_required
def my_profile(request):
    return profile(request, request.user.id)


def register_view(request):
    if request.method == 'POST':
        form = PetUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.pet_name = form.cleaned_data['pet_name']
            user.pet_type = form.cleaned_data['pet_type']
            user.bio = form.cleaned_data['bio']

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = PetUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = PetUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Теперь этот метод доступен
            login(request, user)
            return redirect('index')
    else:
        form = PetUserLoginForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})


def index(request):
    demo_posts = Post.objects.order_by('-created_at')[:3]  # 3 последних поста
    return render(request, 'core/index.html', {
        'demo_posts': demo_posts
    })


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
@require_POST
def toggle_follow(request, user_id):
    target_user = get_object_or_404(PetUser, id=user_id)

    if request.user == target_user:
        return JsonResponse({'status': 'error', 'message': 'Нельзя подписаться на себя'}, status=400)

    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        target=target_user
    )

    if not created:
        subscription.delete()

    return JsonResponse({
        'status': 'ok',
        'is_following': created,
        'followers_count': target_user.followers.count(),
        'following_count': request.user.following.count()
    })


@login_required
def following_feed(request):
    following_ids = request.user.following.values_list('target_id', flat=True)
    posts = Post.objects.filter(author_id__in=following_ids).order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts, 'is_following_feed': True})
