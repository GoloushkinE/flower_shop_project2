from django import template
from django.urls import reverse, resolve
from django.utils.translation import activate, get_language

register = template.Library()

@register.simple_tag(takes_context=True)
def translated_url(context, lang_code):
    request = context['request']
    
    try:
        url_parts = resolve(request.path_info)
        view_name = url_parts.view_name
        kwargs = url_parts.kwargs.copy()
        
        obj = None
        slug_key = None
        if 'category_slug' in kwargs:
            slug_key = 'category_slug'
            obj = context.get('category')
        elif 'slug' in kwargs:
            slug_key = 'slug'
            obj = context.get('product')

        if obj and slug_key:
            try:
                translation_obj = obj.get_translation(lang_code)
                kwargs[slug_key] = translation_obj.slug
            except obj.translations.model.DoesNotExist:
                return f"/{lang_code}/"

        current_lang = get_language()
        activate(lang_code)
        
        url = reverse(view_name, kwargs=kwargs)
        
        activate(current_lang)
        
        return url
        
    except Exception:
        return f"/{lang_code}/"