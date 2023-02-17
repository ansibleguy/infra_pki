from re import sub as regex_replace
from re import search as regex_search
from re import compile as regex_compile


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "valid_domain": self.valid_domain,
            "meets_password_complexity": self.meets_password_complexity,
        }

    @staticmethod
    def safe_key(key: str) -> str:
        return regex_replace('[^0-9a-zA-Z]+', '', key.replace(' ', '_'))

    @staticmethod
    def valid_domain(name: str) -> bool:
        # see: https://validators.readthedocs.io/en/latest/_modules/validators/domain.html
        domain = regex_compile(
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
        )
        return domain.match(name) is not None

    @staticmethod
    def meets_password_complexity(pwd: str, pki_hc: dict) -> bool:
        tests = [
            len(pwd) >= pki_hc['easyrsa']['pwd_min_length'],
            regex_search(r'[0-9]', pwd) is not None,
            regex_search(r'[a-z]', pwd) is not None,
            regex_search(r'[A-Z]', pwd) is not None,
        ]
        return all(tests)
