# -*- coding: utf-8 -*-

import os
import os.path


""" Checking whether this environment is the development or not
Returns:
    bool: True / False
"""


def isDev():
    return os.environ.get("AWS_LAMBDA_FUNCTION_VERSION", "no_env") == "$LATEST"


""" Checking whether this environment is the staging or not
Returns:
    bool: True / False
"""


def isSt():
    return os.environ.get("AWS_LAMBDA_FUNCTION_ALIAS", "no_env") == "st"


""" Checking whether this environment is the production or not
Returns:
    bool: True / False
"""


def isPro():
    return os.environ.get("AWS_LAMBDA_FUNCTION_ALIAS", "no_env") == "pro"


""" Checking whether this environment is staging or development
Returns:
    bool: True / False
"""


def isDevOrSt():
    return isDev() or isSt()


""" Checking whether this environment is the local
Returns:
    bool: True / False
"""


def isLocal():
    return os.environ.get("AWS_LAMBDA_ENV", "no_env") == "local"


""" Checking whether this environment is a docker container
Returns:
    bool: True / False
"""


def isDocker():
    return os.path.exists("/.dockerenv")
