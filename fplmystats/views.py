from django.shortcuts import render
from fplmystats.forms import ContactForm
from django.core.mail import EmailMessage

# TODO fix search boxes on mobile


def index(request):
    contact_form = ContactForm
    context = {'manager_error': False,
               'league_error': False,
               'form': contact_form}
    return render(request, 'index.html', context)


def index_error(request, manager_error, league_error):
    if manager_error == '1':
        manager_error = True
    else:
        manager_error = False
    if league_error == '1':
        league_error = True
    else:
        league_error = False

    contact_form = ContactForm

    context = {'manager_error': manager_error,
               'league_error': league_error,
               'form': contact_form}
    return render(request, 'index.html', context)


def send_comment(request):
    comment_info = request.POST
    name = comment_info['contact_name']
    email = comment_info['contact_email']
    content = comment_info['content']

    email_contents = 'NAME: {}\n\nEMAIL: {}\n\nMESSAGE: {}'.format(name, email, content)
    email = EmailMessage(
        subject='Feedback',
        body=email_contents,
        from_email='info@fplmystats.com',
        to=['info@fplmystats.com'],
        reply_to=['info@fplmystats.com'],
        headers={'Content-Type': 'text/plain'},
    )
    email.send()
    return render(request, 'comment.html')
