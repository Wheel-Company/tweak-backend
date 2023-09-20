
```
tweak-backend
├─ .DS_Store
├─ .gitignore
├─ README.md
├─ api
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ management
│  │  ├─ .DS_Store
│  │  └─ commands
│  │     ├─ .DS_Store
│  │     ├─ grammar_content.xlsx
│  │     ├─ import_category_data.py
│  │     ├─ import_grammar_content_data.py
│  │     ├─ tweak_category.xlsx
│  │     └─ ~$grammar_content.xlsx
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_grammarquestion_category_level_profile_nickname_and_more.py
│  │  ├─ 0003_profile_is_email_registered.py
│  │  ├─ 0004_remove_usergrammarquestion_grammar_question_and_more.py
│  │  ├─ 0005_difficulty_remove_question_question_text_and_more.py
│  │  ├─ 0006_remove_question_question_text_ko_and_more.py
│  │  ├─ 0007_rename_question_grammarcontent_and_more.py
│  │  ├─ 0008_alter_grammarcontent_question_text_en_and_more.py
│  │  ├─ 0009_banner_coupon_expiry_date_grammarcontent_sequence_and_more.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ templates
│  │  ├─ account
│  │  │  ├─ password_reset_email.html
│  │  │  ├─ user_activate_email.html
│  │  │  └─ validation_email.html
│  │  ├─ admin
│  │  │  ├─ excel_upload.html
│  │  │  └─ index.html
│  │  └─ my_note.html
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ config
│  ├─ .DS_Store
│  ├─ dev
│  │  ├─ settings.py
│  │  └─ wsgi.py
│  ├─ middleware.py
│  ├─ production
│  │  └─ settings.py
│  ├─ serializers.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ utils.py
│  └─ views.py
├─ log
├─ manage.py
├─ requirements.txt
└─ static
   ├─ admin
   │  ├─ css
   │  │  ├─ autocomplete.css
   │  │  ├─ base.css
   │  │  ├─ changelists.css
   │  │  ├─ dark_mode.css
   │  │  ├─ dashboard.css
   │  │  ├─ forms.css
   │  │  ├─ login.css
   │  │  ├─ nav_sidebar.css
   │  │  ├─ responsive.css
   │  │  ├─ responsive_rtl.css
   │  │  ├─ rtl.css
   │  │  ├─ vendor
   │  │  │  └─ select2
   │  │  │     ├─ LICENSE-SELECT2.md
   │  │  │     ├─ select2.css
   │  │  │     └─ select2.min.css
   │  │  └─ widgets.css
   │  ├─ img
   │  │  ├─ LICENSE
   │  │  ├─ README.txt
   │  │  ├─ calendar-icons.svg
   │  │  ├─ gis
   │  │  │  ├─ move_vertex_off.svg
   │  │  │  └─ move_vertex_on.svg
   │  │  ├─ icon-addlink.svg
   │  │  ├─ icon-alert.svg
   │  │  ├─ icon-calendar.svg
   │  │  ├─ icon-changelink.svg
   │  │  ├─ icon-clock.svg
   │  │  ├─ icon-deletelink.svg
   │  │  ├─ icon-no.svg
   │  │  ├─ icon-unknown-alt.svg
   │  │  ├─ icon-unknown.svg
   │  │  ├─ icon-viewlink.svg
   │  │  ├─ icon-yes.svg
   │  │  ├─ inline-delete.svg
   │  │  ├─ search.svg
   │  │  ├─ selector-icons.svg
   │  │  ├─ sorting-icons.svg
   │  │  ├─ tooltag-add.svg
   │  │  └─ tooltag-arrowright.svg
   │  └─ js
   │     ├─ SelectBox.js
   │     ├─ SelectFilter2.js
   │     ├─ actions.js
   │     ├─ admin
   │     │  ├─ DateTimeShortcuts.js
   │     │  └─ RelatedObjectLookups.js
   │     ├─ autocomplete.js
   │     ├─ calendar.js
   │     ├─ cancel.js
   │     ├─ change_form.js
   │     ├─ collapse.js
   │     ├─ core.js
   │     ├─ filters.js
   │     ├─ inlines.js
   │     ├─ jquery.init.js
   │     ├─ nav_sidebar.js
   │     ├─ popup_response.js
   │     ├─ prepopulate.js
   │     ├─ prepopulate_init.js
   │     ├─ theme.js
   │     ├─ urlify.js
   │     └─ vendor
   │        ├─ jquery
   │        │  ├─ LICENSE.txt
   │        │  ├─ jquery.js
   │        │  └─ jquery.min.js
   │        ├─ select2
   │        │  ├─ LICENSE.md
   │        │  ├─ i18n
   │        │  │  ├─ af.js
   │        │  │  ├─ ar.js
   │        │  │  ├─ az.js
   │        │  │  ├─ bg.js
   │        │  │  ├─ bn.js
   │        │  │  ├─ bs.js
   │        │  │  ├─ ca.js
   │        │  │  ├─ cs.js
   │        │  │  ├─ da.js
   │        │  │  ├─ de.js
   │        │  │  ├─ dsb.js
   │        │  │  ├─ el.js
   │        │  │  ├─ en.js
   │        │  │  ├─ es.js
   │        │  │  ├─ et.js
   │        │  │  ├─ eu.js
   │        │  │  ├─ fa.js
   │        │  │  ├─ fi.js
   │        │  │  ├─ fr.js
   │        │  │  ├─ gl.js
   │        │  │  ├─ he.js
   │        │  │  ├─ hi.js
   │        │  │  ├─ hr.js
   │        │  │  ├─ hsb.js
   │        │  │  ├─ hu.js
   │        │  │  ├─ hy.js
   │        │  │  ├─ id.js
   │        │  │  ├─ is.js
   │        │  │  ├─ it.js
   │        │  │  ├─ ja.js
   │        │  │  ├─ ka.js
   │        │  │  ├─ km.js
   │        │  │  ├─ ko.js
   │        │  │  ├─ lt.js
   │        │  │  ├─ lv.js
   │        │  │  ├─ mk.js
   │        │  │  ├─ ms.js
   │        │  │  ├─ nb.js
   │        │  │  ├─ ne.js
   │        │  │  ├─ nl.js
   │        │  │  ├─ pl.js
   │        │  │  ├─ ps.js
   │        │  │  ├─ pt-BR.js
   │        │  │  ├─ pt.js
   │        │  │  ├─ ro.js
   │        │  │  ├─ ru.js
   │        │  │  ├─ sk.js
   │        │  │  ├─ sl.js
   │        │  │  ├─ sq.js
   │        │  │  ├─ sr-Cyrl.js
   │        │  │  ├─ sr.js
   │        │  │  ├─ sv.js
   │        │  │  ├─ th.js
   │        │  │  ├─ tk.js
   │        │  │  ├─ tr.js
   │        │  │  ├─ uk.js
   │        │  │  ├─ vi.js
   │        │  │  ├─ zh-CN.js
   │        │  │  └─ zh-TW.js
   │        │  ├─ select2.full.js
   │        │  └─ select2.full.min.js
   │        └─ xregexp
   │           ├─ LICENSE.txt
   │           ├─ xregexp.js
   │           └─ xregexp.min.js
   └─ rest_framework
      ├─ css
      │  ├─ bootstrap-theme.min.css
      │  ├─ bootstrap-theme.min.css.map
      │  ├─ bootstrap-tweaks.css
      │  ├─ bootstrap.min.css
      │  ├─ bootstrap.min.css.map
      │  ├─ default.css
      │  ├─ font-awesome-4.0.3.css
      │  └─ prettify.css
      ├─ docs
      │  ├─ css
      │  │  ├─ base.css
      │  │  ├─ highlight.css
      │  │  └─ jquery.json-view.min.css
      │  ├─ img
      │  │  ├─ favicon.ico
      │  │  └─ grid.png
      │  └─ js
      │     ├─ api.js
      │     ├─ highlight.pack.js
      │     └─ jquery.json-view.min.js
      ├─ fonts
      │  ├─ fontawesome-webfont.eot
      │  ├─ fontawesome-webfont.svg
      │  ├─ fontawesome-webfont.ttf
      │  ├─ fontawesome-webfont.woff
      │  ├─ glyphicons-halflings-regular.eot
      │  ├─ glyphicons-halflings-regular.svg
      │  ├─ glyphicons-halflings-regular.ttf
      │  ├─ glyphicons-halflings-regular.woff
      │  └─ glyphicons-halflings-regular.woff2
      ├─ img
      │  ├─ glyphicons-halflings-white.png
      │  ├─ glyphicons-halflings.png
      │  └─ grid.png
      └─ js
         ├─ ajax-form.js
         ├─ bootstrap.min.js
         ├─ coreapi-0.1.1.js
         ├─ csrf.js
         ├─ default.js
         ├─ jquery-3.5.1.min.js
         └─ prettify-min.js

```