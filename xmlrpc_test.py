import functools
import xmlrpc.client

HOST = 'localhost'
PORT = 8069
DB = 'odoo12'
USER = 'admin'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print("Logged in as %s (uid:%d)" % (USER, uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
sessions = call('odoogoedu.session', 'search_read', [], ['name', 'seats','course_id'])
for session in sessions:
    print("Session %s (%s seats) course_id %s" % (session['name'], session['seats'], session['course_id']))
# 3.create a new session
# session_id = call('odoogoedu.session', 'create', {
#     'name': 'My session',
#     'course_id': 5,
# })
#4.create a new session for the "Functional" course
course_id = call('odoogoedu.course', 'search', [('name','ilike','python')])[0]

session_id = call('odoogoedu.session', 'create', {
    'name' : 'My session',
    'course_id' : course_id,
})
