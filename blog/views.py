import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Uploadfile
from .forms import PostForm, ImageForm
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory

logger = logging.getLogger('django')
#logger.info("HAHA");

#TODO
"""
 1. 외부 에디터 다는 방법 (MD) - OK
 2. 에디터로 작성한 글을 저장.(MD) - OK
 3. 글 포맷에 따라서 포맷팅한 결과를 보여주는 방법 - OK
 7. 페이스북 댓글 플러그인 다는 방법 - OK
 8. 댓글 기능과 현재 post 연결하기 - NO. 그냥 해당 URL과 1:1로 매칭되는 댓글 리스트이다. 관리는 페이스북 개발자 사이트에서 할 수 있다.


 4. 작성과 동시에 미리보기 보는 방법. - 어렵다.. 현재 쓰고있는 플러그인이 지원을 하지 않아서 결국 js로 직접 구현해야 하는데.. 그걸 모르니 ;;;
 5. 하나의 글에 여러개 파일 올리는 방법. - 방법 있는듯.

 6. 외부 에디터와 여러개 파일 업로드 합치는 방법 - 못쓴다. 내부에서 파일 업로드 할때 뭔가 쓰는거 같은데... Django 특성상 token을 같이 줘야 하는데 이걸 못줌.
 7. 리스트 화면에서도 markdown 적용된걸로 나오게 하기
 8. 태그 추가하기

"""

def index(request):
    per_page = 5
    request_page = request.GET.get('page', 1)

    # 모든 Post를 불러온다.
    posts = Post.objects.all()

    # Paginator가 page값에 대한 예외처리를 알아서 하지는 않는다. 예외처리는 별도로 한다.
    pagignator = Paginator(posts, per_page)
    try:
        paged_posts = pagignator.page(request_page)
    except PageNotAnInteger:
        paged_posts = pagignator.page(1)
    except EmptyPage:
        paged_posts = []

    ctx = {
        'posts' : paged_posts,
    }

    return render(request, 'blog/index.html', ctx)


# Create your views here.
def post_list(request):

    per_page = 5
    request_page = request.GET.get('page', 1)

    # 모든 Post를 불러온다.
    posts = Post.objects.all()

    # Paginator가 page값에 대한 예외처리를 알아서 하지는 않는다. 예외처리는 별도로 한다.
    pagignator = Paginator(posts, per_page)
    try:
        paged_posts = pagignator.page(request_page)
    except PageNotAnInteger:
        paged_posts = pagignator.page(1)
    except EmptyPage:
        paged_posts = []

    ctx = {
        'posts' : paged_posts,
    }

    return render(request, 'blog/post_list.html', ctx)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    ctx = {
        'post' : post,
    }

    return render(request, 'blog/post_detail.html', ctx)

def fileupload(request):
    logger.info('파일 업로드 요청')

    form = PostForm()
    if request.method == 'POST':
        logger.info('파일 업로드 POST 요청')

        form = ImageForm(data=request.POST)

        if form.is_valid():
            pass


    ctx = {
        'form' : form,
    }

    return render(request, 'blog/post_edit.html', ctx)


@login_required
def post_write(request):

    form = PostForm()
    imageFormSet = modelformset_factory(Uploadfile, form=ImageForm, extra=2)
    formset = imageFormSet(queryset=Uploadfile.objects.none())

    if request.method == 'POST':
        # Form으로 Validataion 체크하는 방법
        form = PostForm(data=request.POST)
        formset = imageFormSet(request.POST, request.FILES, queryset=Uploadfile.objects.none())

        if form.is_valid() and formset.is_valid():
            new_post = form.save(commit=False)  # commit 인자를 False로 주면 save 호출시 DB에 반영하지는 않고 인스턴스 객체만 리턴한다.
            new_post.user = request.user        # 로그인한 정보를 기입
            new_post.save()                     # DB에 반영

            for form in formset.cleaned_data:
                image = form.get('file')
                if image is not None:
                    photo = Uploadfile(post=new_post, file=image)
                    photo.save()

            url = reverse('blog:detail', kwargs={'pk':new_post.pk})
            return redirect(url)

        else:
            logger.info('잘못됬다.')

    ctx = {
        'form' : form,
        'formset' : formset,
    }

    return render(request, 'blog/post_edit.html', ctx)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect(reverse('blog:detail', kwargs={'pk' : post.pk}))

    ctx = {
        'post' : post,
    }

    return render(request, 'blog/post_edit.html', ctx)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:list')

    return render(request, 'blog/post_delete.html', {'post' : post})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')



def category_list(request):
    pass


def tag_list(request):
    pass


def archive_list(request):
    pass
