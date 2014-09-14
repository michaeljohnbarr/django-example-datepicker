# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
import json
import re

# Django
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.widgets import DateInput
from django.templatetags.static import static
from django.utils.dates import MONTHS_ALT, MONTHS_AP, WEEKDAYS, WEEKDAYS_ABBR
from django.utils.translation import (get_language, get_language_bidi,
                                      ugettext as _)

__all__ = ('DatePickerWidget', )


# ==============================================================================
# CONSTANTS
# ==============================================================================
PYTHON_TO_DATEPICKER_FORMAT = {
    '%d': 'dd',     # day of month (two digit)
    '%j': 'oo',     # day of the year (three digit)
    '%a': 'D',      # day name short
    '%A': 'DD',     # day name long
    '%m': 'mm',     # month of year (two digit)
    '%b': 'M',      # month name short
    '%B': 'MM',     # month name long
    '%y': 'y',      # year (two digit)
    '%Y': 'yy',     # year (four digit)
}


# ==============================================================================
# WIDGETS
# ==============================================================================
class DatePickerWidget(DateInput):
    class Media:
        css = {
            'all': (static('https://code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css'),)
        }
        js = (
            static('https://code.jquery.com/jquery-1.11.1.min.js'),
            static('https://code.jquery.com/ui/1.11.1/jquery-ui.min.js'),
            static('js/jquery.init.js'),
        )

    def __init__(self, attrs=None, format=None, datepicker_class='datepicker',
                 params=None):
        params = params or {}
        attrs = attrs or {}
        class_attr = attrs.get('class', datepicker_class)

        if datepicker_class not in class_attr:
            attrs.update({
                'class': '{0} {1}'.format(class_attr, datepicker_class),
                'readonly': True,
            })
        else:
            attrs.update({
                'class': 'datepicker',
                'readonly': True,
            })

        super(DatePickerWidget, self).__init__(attrs, format)

        self.params = {
            'changeMonth': True,
            'changeYear': True,
            'yearRange': '2000:2050',
        }

        self.regional = {
            'closeText': _('Close'),
            'prevText': _('Previous'),
            'nextText': _('Next'),
            'currentText': _('Current'),
            'monthNames': map(unicode, MONTHS_ALT.values()),
            'monthNamesShort': map(unicode, MONTHS_AP.values()),
            'dayNames': map(unicode, WEEKDAYS.values()),
            'dayNamesShort': map(unicode, WEEKDAYS_ABBR.values()),
            'dayNamesMin': map(unicode, WEEKDAYS_ABBR.values()),
            'isRTL': get_language_bidi(),
            # weekHeader
            # dateFormat
            # firstDay
            # showMonthAfterYear
            # yearSuffix
        }

        # Update the datepicker parameters
        self.params.update(params)

        pattern = re.compile(
            r'(?<!\w)(' + '|'.join(PYTHON_TO_DATEPICKER_FORMAT.keys()) + r')\b'
        )

        if params.get('beforeShowDay'):
            raise NotImplementedError(
                u'beforeShowDay is not supported. Please add the function to '
                u'the template.'
            )

        if not params.get('dateFormat'):
            self.params.update({
                'dateFormat': pattern.sub(
                    lambda x: PYTHON_TO_DATEPICKER_FORMAT[x.group()],
                    self.format
                )
            })

        import datetime
        min_date = self.params.get('minDate')
        if min_date:
            if isinstance(min_date, datetime.date):
                self.params.update({
                    'minDate': self.params['minDate'].strftime(
                        format=self.format
                    )
                })
            elif isinstance(min_date, datetime.datetime):
                self.params.update({
                    'maxDate': min_date.strftime(
                        format=self.format
                    )
                })

        max_date = self.params.get('maxDate')
        if max_date:
            if isinstance(max_date, datetime.date):
                self.params.update({
                    'maxDate': max_date.strftime(
                        format=self.format
                    )
                })
            elif isinstance(max_date, datetime.datetime):
                self.params.update({
                    'maxDate': max_date.strftime(
                        format=self.format
                    )
                })

    def render(self, name, value, attrs=None):
        html = super(DatePickerWidget, self).render(name, value, attrs)
        html += """
            <script type="text/javascript">
                //jQuery(document).ready( function() {
                    var $ = djdp.jQuery;

                    // Retrieve the datepicker based on input name
                    $("#id_%(name)s").datepicker(
                        %(params)s
                    );

                    // Set the custom language/regional options
                    $.datepicker.regional['%(language)s'] = %(regional)s;

                    // Set the region to the region to default
                    $.datepicker.setDefaults($.datepicker.regional[""]);

                    // Set the region to the region options above
                    $.datepicker.setDefaults($.datepicker.regional['%(language)s']);
                //});
            </script>
        """ % {
            'params': json.dumps(self.params, cls=DjangoJSONEncoder),
            'language': get_language(),
            'regional': json.dumps(self.regional, cls=DjangoJSONEncoder),
            'name': name,
        }

        return html
