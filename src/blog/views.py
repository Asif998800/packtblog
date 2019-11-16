from django.shortcuts import render
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'list.html', {'posts': posts})

def post_detail(request, year, month, day, slug):
    post = Post.objects.get(slug=slug,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request, 'detail.html', {'post': post})