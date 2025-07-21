from django import template
from django.urls import resolve
from django.utils.text import capfirst

register = template.Library()

# Diccionario de nombres amigables para breadcrumbs
BREADCRUMB_NAMES = {
    'inicio': 'Inicio',
    'about_us': 'Conocenos',
    'listado libros': 'Libros',
    'listado categorias': 'Categorías',
    'listado autores': 'Autores',
    'nuevo libro': 'Nuevo Libro',
    'editar libro': 'Editar Libro',
    'detalle libro': 'Detalle del Libro',
    'eliminar libro': 'Eliminar Libro',
    'nueva categoria': 'Nueva Categoría',
    'editar categoria': 'Editar Categoría',
    'eliminar categoria': 'Eliminar Categoría',
    'nuevo autor': 'Nuevo Autor',
    'editar autor': 'Editar Autor',
    'eliminar autor': 'Eliminar Autor',
    'login': 'Iniciar Sesión',
}

@register.inclusion_tag('library/partials/breadcrumb.html', takes_context=True)
def render_breadcrumbs(context):
    request = context['request']
    path = request.path.strip('/').split('/')
    breadcrumbs = []

    # No agregar 'Inicio' si la URL actual es exactamente /inicio/
    if path != ['']:
        breadcrumbs.append({
            'name': BREADCRUMB_NAMES.get('inicio', 'Inicio'),
            'url': '/',
            'active': False,
        })

        url_accum = ''
        for i, segment in enumerate(path):
            url_accum = f"{url_accum}/{segment}".replace('//', '/')
            if not url_accum.endswith('/'):
                url_accum += '/'

            try:
                match = resolve(url_accum)
                url_name = match.url_name or segment
                display_name = BREADCRUMB_NAMES.get(url_name, capfirst(url_name.replace('_', ' ')))
                breadcrumbs.append({
                    'name': display_name,
                    'url': None if i == len(path) - 1 else url_accum,
                    'active': (i == len(path) - 1),
                })
            except Exception as e:
                continue

    return {'breadcrumbs': breadcrumbs}
