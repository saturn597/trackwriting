from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Writing
from .forms import WritingForm

from base64 import urlsafe_b64encode
from uuid import uuid4

def index(request):
    context = {}
    if request.user.is_authenticated():
        context['recents'] = Writing.objects.filter(author=request.user).order_by('-time')[:50]
    return render(request, 'storyshare/index.html', context)

def register(request):
    template = 'storyshare/register.html'

    if request.POST:
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
        except KeyError:
            # Somehow a field wasn't filled in
            return render(request, template, {'missing_field': True})


        if User.objects.filter(username=username).exists():
            return render(request, template, {'user_exists': True})

        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, template)

def view_writing(request, id):
    print(id)
    try:
        w = Writing.objects.get(url_id=id)
    except Writing.DoesNotExist:
        w = 'Whoops, not found!'
    return render(request, 'storyshare/viewwriting.html', {'writing': w})

def write(request):
    form = WritingForm()
    errors = []

    url_id = generate_url_id()

    if request.method == 'POST':
        form = WritingForm(request.POST)

        url_id = generate_url_id()
        if not url_id:
            # generate_url_id may return None if it can't find an unused id.
            errors.append('Something odd happened! We recommend you save your'
                    ' work off site.')
        elif form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.url_id = url_id
            story.save()
            return HttpResponseRedirect(reverse('storyshare:index'))

    return render(request, 'storyshare/write.html', {'form': form, 'errors': errors})


def generate_url_id():
    return None
    for _ in range(1, 10):
        url_id = urlsafe_b64encode(uuid4().bytes)[:5]
        if not Writing.objects.filter(url_id=url_id).exists():
            return url_id
    return None
