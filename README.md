Django Form Renderer
====

Testing the `FORM_RENDERER` setting of a Django project, especially in regards to the use of custom widget templates.

[The form rendering API](https://docs.djangoproject.com/en/3.2/ref/forms/renderers/#django.forms.renderers.DjangoTemplates)

The rendering of form templates is controlled by a customizable renderer class. A custom renderer can be specified by updating the FORM_RENDERER setting. It defaults to 'django.forms.renderers.DjangoTemplates'.

#### class DjangoTemplates

This renderer uses a standalone DjangoTemplates engine (unconnected to what you might have configured in the TEMPLATES setting). It loads templates first from the built-in form templates directory in django/forms/templates and then from the installed apps’ templates directories using the app_directories loader.


#### class TemplatesSetting

This renderer gives you complete control of how widget templates are sourced. It uses get_template() to find widget templates based on what’s configured in the TEMPLATES setting.

Using this renderer along with the built-in widget templates requires either:

1. 'django.forms' in INSTALLED_APPS and at least one engine with APP_DIRS=True.

2. Adding the built-in widgets templates directory in DIRS of one of your template engines. To generate that path:

    import django
    django.__path__[0] + '/forms/templates'  # or '/forms/jinja2'

Using this renderer requires you to make sure the form templates your project needs can be located.


See also [ticket #28088](https://code.djangoproject.com/ticket/28088)



### Notes

Add the following to `settings.py`:

    FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'


The `FORM_RENDERER` also controls the loading of widgets with custom paths, not just overriding the default templates.

`TemplatesSetting` will look in any `TEMPLATES` `DIRS` before app-specific code.

To use the standard django forms, `django.forms` must be added to `INSTALLED_APPS`.

Order of `INSTALLED_APPS` matters. For example, during DEBUG mode with `app.apps.AppConfig` listed before `django.forms`:

    Template-loader postmortem

    Django tried loading these templates, in this order:

    Using engine django:
    django.template.loaders.filesystem.Loader: template_loader_bug/templates/widgets/DNE.html (Source does not exist)
    django.template.loaders.app_directories.Loader: .venv/lib/python3.9/site-packages/django/contrib/admin/templates/widgets/DNE.html (Source does not exist)
    django.template.loaders.app_directories.Loader: .venv/lib/python3.9/site-packages/django/contrib/auth/templates/widgets/DNE.html (Source does not exist)
    django.template.loaders.app_directories.Loader: template_loader_bug/app/templates/widgets/DNE.html (Source does not exist)
    django.template.loaders.app_directories.Loader: .venv/lib/python3.9/site-packages/django/forms/templates/widgets/DNE.html (Source does not exist)

Default Django templates can be overridden without specifying a widget subclass with a custom `template_name`, just add the new template under any of the `TEMPLATES` `DIRS` or app templates with a path of `django/forms/widgets`.
