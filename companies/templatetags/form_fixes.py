from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='fix_required_attributes')
def fix_required_attributes(field):
    """
    Template filter to fix required attributes and prevent "True is not defined" errors.
    This filter ensures that Python boolean True values are converted to string "required".
    """
    if not isinstance(field, BoundField):
        return field
    
    # Get the field widget
    widget = field.field.widget
    
    # Check if the field is required
    if getattr(field.field, 'required', False):
        # Ensure required attribute is a string, not boolean
        if hasattr(widget, 'attrs'):
            widget.attrs['required'] = 'required'
            widget.attrs['data-required'] = 'true'
        else:
            widget.attrs = {'required': 'required', 'data-required': 'true'}
    
    return field

@register.filter(name='safe_required')
def safe_required(field):
    """
    Template filter to safely render required attributes.
    Returns 'required' if the field is required, empty string otherwise.
    """
    if not isinstance(field, BoundField):
        return ''
    
    if getattr(field.field, 'required', False):
        return 'required="required"'
    return ''

@register.filter(name='safe_data_required')
def safe_data_required(field):
    """
    Template filter to safely render data-required attributes.
    Returns 'data-required="true"' if the field is required, empty string otherwise.
    """
    if not isinstance(field, BoundField):
        return ''
    
    if getattr(field.field, 'required', False):
        return 'data-required="true"'
    return ''
