from flask_debugtoolbar import DebugToolbarExtension

from app import app

app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
toolbar = DebugToolbarExtension(app)

if __name__ == '__main__':
    # app.run('0.0.0.0', 8085)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    app.run(debug=True, use_debugger=True, use_reloader=True)
