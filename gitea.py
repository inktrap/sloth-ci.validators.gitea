

__title__ = 'sloth-ci.validators.gitlab'
__description__ = 'GitLab validator for Sloth CI'
__version__ = '1.0.2'
__author__ = 'Vladimir Akritskiy'
__author_email__ = 'lenin.lin@gmail.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Check payload from GitLab: the origin IP must be genuine and the repo title must be valid.

    :param request: `CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html#cherrypy._cprequest.Request>`_ instance representing incoming request
    :param validation_data: dict with the keys ``trusted_ips``, ``repo``, and ``branches``, parsed from the config

    :returns: namedtuple(status, message, list of extracted params as dicts), e.g. ``Response(status=200, message='Payload validated. Branches: default', [{'branch': 'default'}])``
    '''

    from collections import namedtuple


    response = namedtuple('Response', ('status', 'message', 'param_dicts'))

    if request.method != 'POST':
        return response(405, 'Payload validation failed: Wrong method, POST expected, got %s.' % request.method, [])

    if request.remote.ip not in validation_data['trusted_ips']:
        return response(403, 'Payload validation failed: Unverified remote IP: %s.' % remote_ip, [])

    try:
        payload = request.json

        repo = payload['repository']['name']

        if repo != validation_data['repo']:
            return response(403, 'Payload validation failed: wrong repository: %s' % repo, [])

        branch = {payload['ref'].split('/')[-1]}

        allowed_branches = set(validation_data.get('branches', branch))

        if not branch & allowed_branches:
            return response(403, 'Payload validation failed: wrong branch: %s' % branch, [])

        return response(200, 'Payload validated. Branch: %s' % branch, [{'branch': branch}])

    except Exception as e:
        return response(400, 'Payload validation failed: %s' % e, [])
