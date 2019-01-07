from django.core.mail import EmailMessage
from blog.celery import app


@app.task
def send_post_email(sub_list, post_title, slug):
    for sub in sub_list:
        email = EmailMessage(subject='Новый пост на Seems Good Blog!',
                             body='В моем блоге новый пост: <a href="http://seemsgoodblog.ru'
                                  '/post/{}">{}</a><br><br><br>Чтобы отписаться от рассылки '
                                  'перейдите по <a href="http://seemsgoodblog.ru/unsubscribe/{}">ссылке</a>'
                             .format(slug, post_title, sub.get('unsub_key')),
                             to=[sub.get('email')]
                             )
        email.content_subtype = "html"
        email.send()
