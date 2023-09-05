
```
tweak-backend
├─ .DS_Store
├─ .gitignore
├─ Dockerfile
├─ README.md
├─ api
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ management
│  │  ├─ .DS_Store
│  │  └─ commands
│  │     ├─ import_category_data.py
│  │     ├─ import_questions_data.py
│  │     ├─ questions.xlsx
│  │     ├─ tweak_category.xlsx
│  │     └─ ~$questions.xlsx
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_grammarquestion_category_level_profile_nickname_and_more.py
│  │  ├─ 0003_profile_is_email_registered.py
│  │  ├─ 0004_remove_usergrammarquestion_grammar_question_and_more.py
│  │  ├─ 0005_difficulty_remove_question_question_text_and_more.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ templates
│  │  ├─ account
│  │  │  ├─ password_reset_email.html
│  │  │  ├─ user_activate_email.html
│  │  │  └─ validation_email.html
│  │  └─ admin
│  │     ├─ excel_upload.html
│  │     └─ index.html
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ backend
│  ├─ .DS_Store
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings
│  │  ├─ base.py
│  │  ├─ dev.py
│  │  └─ prod.py
│  ├─ urls.py
│  ├─ utils.py
│  ├─ views.py
│  └─ wsgi.py
├─ manage.py
└─ requirements.txt

```