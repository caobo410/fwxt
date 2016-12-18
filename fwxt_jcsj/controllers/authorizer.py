import rest
import functools
from psycopg2 import OperationalError
from openerp.exceptions import except_orm, ValidationError


def authorize(f):

    @functools.wraps(f)
    def wrap(controller, **kwargs):
        try:
            env = rest.check_token('fwxt', 'admin', '1')
            if not env:
                return rest.unauthorized()
            else:
                controller.current_env = env
            return f(controller, **kwargs)
        except OperationalError, e:
            return rest.bad_request(str(e))
        except TypeError, e:
            return rest.bad_request(str(e))
        except ValidationError, e:
            return rest.bad_request(str(e))
        except except_orm, e:
            return rest.bad_request(str(e))

    return wrap
