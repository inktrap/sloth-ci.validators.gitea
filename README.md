# sloth-ci.validators.gitea

Sloth CI validator for [Gitea](https://gitea.io.com/) [push](https://docs.gitea.io/en-us/webhooks/) events.
Gitea sends the same [payload data](https://docs.gitea.io/en-us/webhooks/) triggered by push hooks as GitHub.

TODO: ipv6?
```
            - 2a03:4000:4c:e24:85e:10ff:fef8:a405
```

## Installation

```
$ pip install sloth-ci.validators.gitea
```


## Usage

```
provider:
    gitea:
        # Repository owner. Mandatory parameter.
        owner: moigagoo
        # Whitelisted Gitea server IPs. Mandatory parameter.
        # This is only codeberg.org and localhost by default
        # but must be extended as you see fit if you self-host Gitea
        trusted_ips:
            - 193.26.156.135
            - 127.0.0.1

        # Repository title as it appears in the URL, i.e. slug.
        # Mandatory parameter.
        repo: sloth-ci

        # Only pushes to these branches will initiate a build.
        # Skip this parameter to allow all branches to fire builds.
        branches:
            - master
            - staging
```

