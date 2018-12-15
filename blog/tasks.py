from django.core.mail import EmailMessage
from blog.celery import app


@app.task
def send_post_email(sub_emails, post_title, slug):
    if sub_emails:
        email = EmailMessage(subject='Новый пост на Seems Good Blog!',
                             body='В моем блоге новый пост: <a href="http://127.0.0.1:8000'
                                  '/post/{}">{}</a>'.format(slug, post_title),
                             to=sub_emails
                             )
        email.send()
