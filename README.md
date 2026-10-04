# KUHIN PHP Website

The production application in this repository is the plain PHP + MySQL/MariaDB site under [`php_version/`](php_version/). It runs on Apache/PHP shared hosting and has no Python, Django, Node.js, Docker, Gunicorn, or Redis runtime dependency.

## Start Here

- PHP setup, requirements, database import, security, and local smoke test: [`php_version/README.md`](php_version/README.md)
- University shared hosting steps: [`DEPLOYMENT.md`](DEPLOYMENT.md)
- PHP/database/Apache compatibility: [`HOSTING_COMPATIBILITY.md`](HOSTING_COMPATIBILITY.md)
- Hosting handoff checklist: [`UNIVERSITY_HOSTING_CHECKLIST.md`](UNIVERSITY_HOSTING_CHECKLIST.md)
- Final migration and deployment audit: [`FINAL_MIGRATION_AUDIT.md`](FINAL_MIGRATION_AUDIT.md)
- Source feature mapping: [`DJANGO_TO_PHP_FUNCTIONALITY_MATRIX.md`](DJANGO_TO_PHP_FUNCTIONALITY_MATRIX.md)
- Cleanup classification: [`DJANGO_CLEANUP_PLAN.md`](DJANGO_CLEANUP_PLAN.md)

## Local Preview

From `php_version/`, configure a MySQL database using `database/schema.sql`, copy `.env.example` to `.env`, install PHPMailer with Composer, and run:

```sh
php -S 127.0.0.1:8000 -t . router.php
```

When this workspace is opened in VS Code, the local PHP server starts automatically after automatic tasks are allowed. Open <http://127.0.0.1:8000>. This development server is for local use only; production must use the hosting provider's Apache/PHP setup and production environment settings.

The local verification database used during migration audit was disposable and is not application production data.

## Migration Artifacts

`db.sqlite3` and the root `media/` directory are retained as private migration/recovery sources for `php_version/database/migrate_data.php`. They are not part of the PHP runtime package and must not be uploaded into `public_html`. The PHP application uses its own `php_version/uploads/` and copied assets.

The university-provided specifications were placeholders during the audit. Do not cut over from the existing Django backup until the actual PHP version, extensions, database, Apache rewrite policy, uploads, and SMTP have been verified using the hosting checklist.
# PHP_kuhin
