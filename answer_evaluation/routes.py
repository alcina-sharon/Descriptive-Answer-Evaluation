def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('first', '/first')
    config.add_route('register', '/register')
    config.add_route('signin', '/signin')
    config.add_route('page','/page')
    config.add_route('pg','/pg')
    config.add_route('taketest','/taketest')
    config.add_route('allresults','/allresults')
    config.add_route('createtest','/createtest')
    config.add_route('nxt','/nxt')
    config.add_route('veiwresult','/veiwresult')
    config.add_route('save','/save')
    config.add_route('tt','/tt')
    config.add_route('3t','/3t')
    config.add_route('4t','/4t')
    