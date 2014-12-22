
import six


def model_from_content(model_class, content, key_are_value=False):
    if isinstance(content, dict):
        key = list(content.keys())[0]
        if key_are_value:
            return model_class(key, content[key])
        else:
            if isinstance(content[key], dict):
                return model_class(key, **content[key])
            elif isinstance(content[key], (list, tuple)):
                return model_class(key, content[key])
            else:
                return model_class(**content)

    elif isinstance(content, (list, tuple)):
        return model_class(content)


def wrap_result(model_class, multiple=False, key_are_value=False):
    def _wrap_model(func):
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)

            if multiple:
                result = []

                if isinstance(content, (list, tuple)):
                    for item in content:
                        result.append(model_from_content(model_class, item, key_are_value))

                elif isinstance(content, dict):
                    for key, value in six.iteritems(content):
                        result.append(model_from_content(model_class, {key: value}, key_are_value))

                return result

            else:
                return model_from_content(model_class, content, key_are_value)

        return wrapper
    return _wrap_model