# sloth-ci.validators.gitea

Sloth CI validator for [Gitea](https://gitea.io.com/) [push](https://docs.gitea.io/en-us/webhooks/) events.


## Installation

```
$ pip install sloth-ci.validators.gitea
```


## Usage

```
provider:
    gitea:
        # Whitelisted Gitea server IPs.
        # Optional parameter, since Gitea is a self-hosted service or might be
        # used via e.g. codeberg.org
        trusted_ips:
            - 123.45.67.89
            - 111.22.33.44

        # Repository title as it appears in the URL, i.e. slug.
        # Mandatory parameter.
        repo: sloth-ci

        # Only pushes to these branches will initiate a build.
        # Skip this parameter to allow all branches to fire builds.
        branches:
            - master
            - staging
```

