from re import sub as regex_replace
from re import search as regex_search
from re import compile as regex_compile


class FilterModule(object):

    def filters(self):
        return {
            "safe_key": self.safe_key,
            "valid_domain": self.valid_domain,
            "meets_password_complexity": self.meets_password_complexity,
            "build_san": self.build_san,
            "ensure_list": self.ensure_list,
            "is_dict": self.is_dict,
            "unique_bases": self.unique_bases,
            "san_cs_dict": self.san_cs_dict,
            "is_var_string": self.is_var_string,
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

    @staticmethod
    def ensure_list(data: (str, dict, list)) -> list:
        # if user supplied a string instead of a list => convert it to match our expectations
        if isinstance(data, list):
            return data

        return [data]

    @classmethod
    def build_san(cls, cert: dict, san_mapping: dict) -> str:
        san = []

        if 'san' in cert:
            for ansible_key, openssl_key in san_mapping.items():
                if ansible_key in cert['san']:
                    for entry in cls.ensure_list(cert['san'][ansible_key]):
                        openssl_key_value = f'{openssl_key}:{entry}'
                        if openssl_key_value not in san:
                            san.append(openssl_key_value)

                if openssl_key != ansible_key and openssl_key in cert['san']:
                    for entry in cls.ensure_list(cert['san'][openssl_key]):
                        openssl_key_value = f'{openssl_key}:{entry}'
                        if openssl_key_value not in san:
                            san.append(openssl_key_value)

        if len(san) == 0:
            return ''

        return f"\"{','.join(san)}\""

    @staticmethod
    def is_dict(data) -> bool:
        return isinstance(data, dict)

    @staticmethod
    def unique_bases(instances: dict, default: str) -> list:
        bases = []

        for i in instances:
            if 'path_base' in i:
                bases.append(i['path_base'])
            else:
                bases.append(default)

        return list(set(bases))

    @staticmethod
    def san_cs_dict(data: str) -> dict:
        san = {}

        for entry in data.split(','):
            key, value = entry.split(':')
            if key not  in san:
                san[key] = []

            san[key].append(value)

        return san

    @staticmethod
    def is_var_string(data: (str, int, None)) -> bool:
        if isinstance(data, str):
            if data not in ['yes', 'no']:
                return True

        return False
