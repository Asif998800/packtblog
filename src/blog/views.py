from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# Create your views here.

# class PostListView(ListView):
#     queryset = Post.objects.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'list.html'

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')

    # Handle out of range and invalid page numbers:
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'list.html',{'posts': posts})

def post_detail(request, year, month, day, slug):
    post = Post.objects.get(slug=slug,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'detail.html', {'post': post, 
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form})

def post_share(request, id):
    post = get_object_or_404(Post, id=id)
    sent = False

    form = EmailPostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                        post.get_absolute_url())
            subject = '{} ({}) recommends you reading "\
{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:'.format(post.title, post_url, cd['name'])
            send_mail(subject, message, 'asif018600@gmail.com',
[cd['to']])
            sent = True
        else:
            form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form, 'sent': sent})


