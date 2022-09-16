from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin


def search_posts(request):
    if request.method == "POST":
        searched = request.POST.get('searched','')
        posts = Post.objects.filter(content__contains=searched)
        return render(request, 'search_posts.html',
        {'searched':searched, 'posts':posts})
    else:
        return render(request, 'search_posts.html',
        {})


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get_post_details(self, slug):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = post.likes.filter(id=self.request.user.id).exists()
        return {
            "post": post,
            "comments": comments,
            "liked": liked,
        }

    def get(self, request, slug, *args, **kwargs):
        details = self.get_post_details(slug)
        return render(
            request,
            "post_detail.html",
            {
                "commented": False,
                "comment_form": CommentForm(),
                **details  # unpack dict into this dictionary
            },
        )

    def post(self, request, slug, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(_lazy("login"))

        details = self.get_post_details(slug)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()    

        return render(
            request,
            "post_detail.html",
            {
                "commented": True,
                "comment_form": CommentForm(),
                **details
            },
        )

class PostLike(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    redirect_field_name = 'redirect_to'

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        return HttpResponseRedirect(reverse_lazy('post_detail', args=[slug]))


    