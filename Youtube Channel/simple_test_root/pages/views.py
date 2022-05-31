from django.shortcuts import render
# from django.http import HttpResponse
from . models import Page
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection
from django.urls import reverse
from .contact import ContactForm
from datetime import date

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            con = get_connection('django.core.mail.backends.console.EmailBackend')
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@dcu.ie'),
                ['student@dcu.ie'], # change this
                connection=con
            )
            return HttpResponseRedirect(reverse('contact') + '?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'form': form,
        'page_list': Page.objects.all(),
        'submitted': submitted
    }
    return render(request, 'pages/contact.html', context)

def index(request, pagename = ''):
    pagename = '/' + pagename
    pg = Page.objects.get(permalink=pagename)
    t = date.today()
    month = t.strftime('%b')
    year = t.year
    context = {
    'title': pg.title,
    'content': pg.bodytext,
    'last_updated': pg.update_date,
    'page_list': Page.objects.all(),
    'welcome': f'Welcome to {month} {year}',
    }

    return render(request, 'pages/page.html', context)
