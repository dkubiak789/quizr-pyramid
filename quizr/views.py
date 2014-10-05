import random
import time
import formencode

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from pyramid.view import view_config
from pyramid.renderers import render

from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry

from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)

from .models import (
    DBSession,
    User,
    Result,
)

from .utils import ANSWER_IDS, get_questions


@view_config(permission='view', route_name='main',
             renderer='templates/main.pt')
def main_view(request):
    login_form = login_form_view(request)

    username = authenticated_userid(request)
    if request.method == 'POST' and username:
        filename = get_current_registry().settings['questions_csv']
        questions = get_questions(filename)
        request.session['points'] = 0
        request.session['to_ask'] = random.sample(questions, 5)
    
        return HTTPFound(location=request.route_url('question'))

    return {
        'username': username,
        'toolbar': toolbar_view(request),
        'login_form': login_form,
    }


class RegistrationSchema(formencode.Schema):
    allow_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)
    password = formencode.validators.PlainText(not_empty=True)
    email = formencode.validators.Email(resolve_domain=False)
    name = formencode.validators.String(not_empty=True)
    password = formencode.validators.String(not_empty=True)
    confirm_password = formencode.validators.String(not_empty=True)
    chained_validators = [
        formencode.validators.FieldsMatch('password', 'confirm_password')
    ]


@view_config(permission='view', route_name='register',
             renderer='templates/user_add.pt')
def user_add(request):

    form = Form(request, schema=RegistrationSchema)

    if 'form.submitted' in request.POST and form.validate():
        session = DBSession()
        username = form.data['username']
        user = User(
            username=username,
            password=form.data['password'],
            name=form.data['name'],
            email=form.data['email']
        )
        session.add(user)

        headers = remember(request, username)

        redirect_url = request.route_url('main')

        return HTTPFound(location=redirect_url, headers=headers)

    login_form = login_form_view(request)

    return {
        'form': FormRenderer(form),
        'toolbar': '',
        'login_form': '',
    }


@view_config(permission='view', route_name='login')
def login_view(request):
    main_view = request.route_url('main')
    came_from = request.params.get('came_from', main_view)

    post_data = request.POST
    if 'submit' in post_data:
        login = post_data['login']
        password = post_data['password']

        if User.check_password(login, password):
            headers = remember(request, login)
            request.session.flash(u'Logged in successfully.')
            return HTTPFound(location=came_from, headers=headers)

    request.session.flash(u'Failed to login.')
    return HTTPFound(location=came_from)


@view_config(permission='post', route_name='logout')
def logout_view(request):
    request.session.invalidate()
    request.session.flash(u'Logged out successfully.')
    headers = forget(request)
    return HTTPFound(location=request.route_url('main'), headers=headers)


def toolbar_view(request):
    viewer_username = authenticated_userid(request)
    return render(
        'templates/toolbar.pt',
        {'viewer_username': viewer_username},
        request
    )


def login_form_view(request):
    logged_in = authenticated_userid(request)
    return render('templates/login.pt', {'loggedin': logged_in}, request)


@view_config(permission='post', route_name='question',
             renderer='templates/question.pt')
def question_page(request):
    """
    Quiz question page - show question, handle answer.
    """
    session = request.session
    if request.method == 'POST':
        if request.POST.get('answer') == session['correct_answer']:
            diff_time = time.time() - session['start_time']
            if diff_time < 10:
                session['points'] += 3
            elif diff_time < 30:
                session['points'] += 2
            else:
                session['points'] += 1
        if not session['to_ask']:
            return HTTPFound(location=request.route_url('result'))
        else:
            return HTTPFound(location=request.route_url('question'))
    else:
        if not session['to_ask']:
            return HTTPFound(location=request.route_url('result'))
        question = session['to_ask'].pop()
        session['correct_answer'] = question[-1]
        session['start_time'] = time.time()
        return {
            'question': question[0],
            'answers': zip(ANSWER_IDS, question[1:-1]),
            'toolbar': toolbar_view(request),
        }


@view_config(permission='post', route_name='result',
             renderer='templates/result.pt')
def result_page(request):
    """
    Last page - show results.
    """
    session = request.session
    points = None
    
    if 'points' in session:
        points = session['points']
        del session['points']
    
        username = authenticated_userid(request)
        user_id = DBSession.query(User).\
                            filter(User.username==username).\
                            first().user_id
        
        result = Result(user_id=user_id, points=points)
        DBSession.add(result)
    
    results = DBSession.query(Result, User).\
                        join(User).\
                        order_by(Result.points.desc()).\
                        all()

    return {
        'points': points,
        'toolbar': toolbar_view(request),
        'results': results,
    }