from flask import Blueprint, render_template, request, session, redirect, url_for, Response
import subprocess, os

main_bp = Blueprint('main', __name__)

SCRIPTS = {
    'percentage': os.path.join('project-root', 'scripts', 'update_prices_shopify.py'),
    'variant': os.path.join('tempo solution', 'update_prices.py')
}


def login_required(view):
    from functools import wraps
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped

@main_bp.route('/')
@login_required
def home():
    return render_template('home.html')

@main_bp.route('/percentage-updater')
@login_required
def percentage_updater():
    return render_template('percentage.html')

@main_bp.route('/variant-updater')
@login_required
def variant_updater():
    return render_template('variant.html')


def stream_process(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(process.stdout.readline, ''):
        yield f'data: {line.rstrip()}\n\n'
    process.wait()
    yield 'data: --done--\n\n'

@main_bp.route('/stream/percentage')
@login_required
def stream_percentage():
    percent = request.args.get('percent')
    if not percent:
        return 'Missing percent', 400
    cmd = ['python3', SCRIPTS['percentage'], '--percent', percent]
    return Response(stream_process(cmd), mimetype='text/event-stream')

@main_bp.route('/stream/variant')
@login_required
def stream_variant():
    cmd = ['python3', SCRIPTS['variant']]
    return Response(stream_process(cmd), mimetype='text/event-stream')
