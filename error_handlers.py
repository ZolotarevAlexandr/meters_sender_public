from flask import render_template, Blueprint

blueprint = Blueprint(
    'error_handlers',
    __name__,
    template_folder='templates'
)


@blueprint.app_errorhandler(404)
def error_404(e):
    return render_template('error.html', error_name='Запрашиваемая страница не найдена')


@blueprint.app_errorhandler(401)
def error_401(e):
    return render_template('error.html', error_name='Войдите в аккаунт для доступа к странице')
