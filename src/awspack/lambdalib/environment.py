# -*- coding: utf-8 -*-

import os


""" Checking whether this environment is the development or not
Returns:
    bool: True / False
"""


def isDev() -> bool:
    return os.environ.get("AWS_LAMBDA_FUNCTION_VERSION", "no_env") == "$LATEST"


""" Checking whether this environment is the staging or not
Returns:
    bool: True / False
"""


def isSt() -> bool:
    return os.environ.get("AWS_LAMBDA_FUNCTION_ALIAS", "no_env") == "st"


""" Checking whether this environment is the production or not
Returns:
    bool: True / False
"""


def isPro() -> bool:
    return os.environ.get("AWS_LAMBDA_FUNCTION_ALIAS", "no_env") == "pro"


""" Checking whether this environment is staging or development
Returns:
    bool: True / False
"""


def isDevOrSt() -> bool:
    return isDev() or isSt()


""" Checking whether this environment is local.
Returns:
    bool: True / False
"""


def isLocal() -> bool:
    if os.environ.get("AWS_LAMBDA_FUNCTION_VERSION", "no_env") == "no_env":
        return True
    return os.environ.get("AWS_LAMBDA_ENV", "no_env") == "local"


""" Checking whether this environment is a docker container
Returns:
    bool: True / False
"""


def isDocker() -> bool:
    return os.path.exists("/.dockerenv")
