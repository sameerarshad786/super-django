from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    
    if filesize > 1024 * 1024:
        raise ValidationError("You cannot upload file more than 10Mb")
    else:
        return value
