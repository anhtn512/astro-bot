import re


def check_get_proposals(message):
    regex = "(?i)^proposalsfrom \d+"
    if re.match(regex, message, flags=re.UNICODE):
        return True
    return False


def check_get_approved(message):
    regex = "(?i)^approvedsfrom \d+"
    if re.match(regex, message, flags=re.UNICODE):
        return True
    return False


def check_help_bot(message):
    regex = "(?i)^help$"
    if re.match(regex, message, flags=re.UNICODE): return True
    return False