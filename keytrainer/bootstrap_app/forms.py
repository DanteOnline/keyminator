def set_form_control(fields):
    for field in fields.values():
        field.widget.attrs['class'] = 'form-control'