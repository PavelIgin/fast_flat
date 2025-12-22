class OnlyForOwnerException(Exception):
    message = "You should be owner for this request"
    http_code = 403
