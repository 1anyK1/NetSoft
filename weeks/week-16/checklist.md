# Чек-лист OWASP Top 10 (Web) для devices-s01 — 13 пунктов

1. Injection (SQL/NoSQL/Command): параметризовать запросы, не смешивать пользовательские строки в shell.
2. Broken Authentication / Session mgmt., проверка JWT/expiry/brute-force throttling.
3. Sensitive Data Exposure: TLS, не логировать PII/token.
4. XML External Entities (XXE): не парсить ненужный XML с внешними сущностями.
5. Broken Access Control: проверка owner/tenant на каждое изменение ресурса.
6. Security Misconfiguration: заголовки, дефолтные пароли выключены, debug=False.
7. XSS: экранировать HTML/использовать CSP.
8. Insecure Deserialization: не использовать pickle на недоверенных данных.
9. Using Components With Known Vulnerabilities: CVE-сканы зависимостей/image.
10. Insufficient Logging & Monitoring: безопасные audit logs + алертинг по 5xx/abuse patterns.
11. SSRF при вызове внешних URL по данным клиента — белые списки.
12. Mass assignment / переопределение полей статусов при PATCH.
13. Rate limiting на публичных эндпоинтах (anti-bruteforce, anti-abuse).

# Audit использование

Отметить ✓ после ручной проверки каждого пункта и занести вывод в `audit.md`.
