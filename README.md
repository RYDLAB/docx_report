# DOCS report

Позволяет добавлять в модель отчётов новый шаблон-источник файл формата docx.  
Получить отчёты на основе такого шаблона можно в формате docx или pdf.  
Для преобразования docx -> pdf требуется доступный сервис gotenberg на localhost:8808.  
Пример запуска сервиса в docker-compose рядом с Odoo:

```yaml
gotenberg:
    image: thecodingmachine/gotenberg:6
    restart: unless-stopped
    environment:
        LOG_LEVEL: INFO
        DEFAULT_LISTEN_PORT: 8808
        DISABLE_GOOGLE_CHROME: 1
        DEFAULT_WAIT_TIMEOUT: 30
        MAXIMUM_WAIT_TIMEOUT: 60
```
