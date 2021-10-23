# TODO: check for headers
# X-Gitea-Delivery: f6266f16-1bf3-46a5-9ea4-602e06ead473
# X-Gitea-Event: push
# see: <https://docs.gitea.io/en-us/webhooks/>


def validate(request, validation_data):
    """Check payload from Gitea: the origin IP must be genuine; the repo owner and title must be valid.

    :param request: `CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html#cherrypy._cprequest.Request>`_ instance representing incoming request
    :param validation_data: dict with the keys ``owner`` ``trusted_ips``, ``repo``, and ``branches``, parsed from the config

    :returns: namedtuple(status, message, list of extracted params as dicts), e.g. ``Response(status=200, message='Payload validated. Branches: default', [{'branch': 'default'}])``

    """

    from collections import namedtuple

    from ipaddress import ip_address, ip_network

    response = namedtuple("Response", ("status", "message", "param_dicts"))

    if request.method != "POST":
        return response(
            405,
            "Payload validation failed: Wrong method, POST expected, got %s."
            % request.method,
            [],
        )

    this_header = "X-Gitea-Delivery"
    if this_header not in request.header:
        return response(
            403,
            "Header validation failed: Header not present: %s" % this_header,
            [],
        )

    this_header = "X-Gitea-Event"
    if this_header not in request.header:
        return response(
            403,
            "Header validation failed: Header not present: %s" % this_header,
            [],
        )

    # remote_ip = ip_address(request.remote.ip)
    if request.remote.ip not in validation_data["trusted_ips"]:
        return response(
            403,
            "Payload validation failed: Unverified remote IP: %s." % request.remote.ip,
            [],
        )

    try:
        payload = request.json

        is_ping = "zen" in payload

        if is_ping:
            owner = payload["repository"]["owner"]["login"]
        else:
            owner = payload["repository"]["owner"]["name"]

        if owner != validation_data["owner"]:
            return response(
                403, "Payload validation failed: wrong owner: %s" % owner, []
            )

        repo = payload["repository"]["name"]

        if repo != validation_data["repo"]:
            return response(
                403, "Payload validation failed: wrong repository: %s" % repo, []
            )

        if is_ping:
            return response(200, "Ping payload validated", [])

        branch = payload["ref"].split("/")[-1]

        allowed_branches = set(validation_data.get("branches", branch))

        if branch not in allowed_branches:
            return response(
                403, "Payload validation failed: wrong branch: %s" % branch, []
            )

        return response(
            200, "Payload validated. Branch: %s" % branch, [{"branch": branch}]
        )

    except Exception as e:
        return response(400, "Payload validation failed: %s" % e, [])
