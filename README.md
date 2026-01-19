from django.conf.global_settings import MEDIA_URL

# djangorealtime
Apliação em tempo real com Django

Pacote a serem instalados

- Django
- Django Channels
- Redis
- Bootstrap (opcional para estilização)
- Channel Layers para Redis

## Instalação
```commandline
    pip install django django-channels django-bootstrap4 channels-redis
```

Requirements.txt
```commandline
    pip freeze > requirements.txt
```

## Configuração do Projeto
1. Crie um novo projeto Django:
```commandline
    django-admin startproject djangorealtime .
```
2. Crie um novo aplicativo dentro do projeto:
```commandline
    python manage.py startapp chat
```
3. Adicione os aplicativos instalados no arquivo `settings.py`:

+ Definição dos aplicativos instalados no arquivo settings.py
    ```python
        INSTALLED_APPS = [
            ...
            'channels',
            'chat',
            'bootstrap4',
        ]
    ```
+ Configuração do diretório de templates no arquivo settings.py
    ```python
        TEMPLATES = [
            {
                ...
                'DIRS': ['templates'],
                ...
            },
        ]
    ```
+ Definição da linguagem padrão no arquivo settings.py
    ```python
        LANGUAGE_CODE = 'pt-br'
    ```
+ Definição do timezone no arquivo settings.py
    ```python
        TIME_ZONE = 'America/Sao_Paulo'
    ```
+ Definição dos diretórios estáticos no arquivo settings.py
    ```python
        STATIC_URL = '/static/'
        STATICFILES_DIRS = os.path.join(BASE_DIR,'staticfiles'),
    ```
+ Definição do diretório de mídia no arquivo settings.py
    ```python
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    ```
+ Configuração do Channels no arquivo settings.py
    ```python
        ASGI_APPLICATION = 'djangorealtime.routing.application'

        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    'hosts': [('127.0.0.1', 6379)],
                },
            },
        }
  ```
4. Configuração do arquivo de urls.py do projeto:
```python
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('chat.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

5. COnfiguração do arquivo urls.py do app chat:
```python
    from django.urls import path
    from .views import IndexView, SalaView
    
    urlpatterns = [
        path('', IndexView.as_view(), name='index'),
        path('chat/<str:nome_sala>/', SalaView.as_view(), name='sala'),
    ]
```

6. Crie o arquivo routing.py na pasta do projeto:
```python
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    import chat.routing

    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
    })
```