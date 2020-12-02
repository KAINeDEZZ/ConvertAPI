import json


class ParseException(Exception):
    def __init__(self, parsed_url:  str):
        self.parsed_url = parsed_url

    def convert_to_json(self):
        return {
            'code': 500,
            'body': {json.dumps({'error': f'An exception or invalid data was'
                                          f' received during parsing resource {self.parsed_url}.'})}
        }


class GetTableFromWebException(Exception):
    def __init__(self, parsed_url:  str):
        self.parsed_url = parsed_url

    def convert_to_json(self):
        return {
            'code': 500,
            'body': {json.dumps({'error': f'Can\'t get data from middleware resource: {self.parsed_url}.'})}
        }


class AtypicalException(Exception):
    def __init__(self, exception: Exception, module: str):
        self.exception = exception
        self.module = module
        print(self.module, type(self.exception), self.exception)

    def convert_to_json(self):
        return {
            'status': 500,
            'body': json.dumps({'error': f'Caught atypical error in {self.module}:'
                                         f' {type(self.exception)} {self.exception.args}'})
        }


class ArgumentsNotFoundException(Exception):
    def __init__(self, not_found_arguments: list):
        self.not_found_arguments = not_found_arguments
        print(self.not_found_arguments)

    def convert_to_json(self):
        return {
            'status': 400,
            'body': json.dumps({'error': f'Arguments {self.not_found_arguments} not found.'})
        }


class InvalidArgumentException(Exception):
    def __init__(self, invalid_argument: str, message: str):
        self.invalid_argument = invalid_argument
        self.message = message

    def convert_to_json(self):
        return {
            'status': 400,
            'body': json.dumps({'error': f'Invalid value for {self.invalid_argument}, {self.message}.'})
        }
