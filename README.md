django-example-datepicker
=========================

Sample Datepicker app

One of the vexing parts of using jQuery's DatePicker is that it supports languages, but not all languages that Django supports. Thus, I created a widget which utilizes Django's translations to override the regional settings provided by jQuery's DatePicker.

The aim is to have the benefit of localized date formats and language strings based on Django's localization!

To test with simple localization, change the `settings.LANGUAGE_CODE`
