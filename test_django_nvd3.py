# Copyright (c) 2016 Marco Giusti
# Copyright (c) 2013-2014 Arezqui Belaid <areski@gmail.com> and other
# contributors
# See LICENSE.txt for details.

import unittest

from django.conf import settings
settings.configure(INSTALLED_APPS=["django_nvd3"])
import django
django.setup()
from django.template import Context, Template
from django.test.utils import override_settings
from django_nvd3.templatetags.nvd3_tags import load_chart, include_container


HEADER = u"""\
<link media="all" href="{css}" type="text/css" rel="stylesheet" />
<script src="{d3js}" type="text/javascript" charset="utf-8"></script>
<script src="{nvd3js}" type="text/javascript" charset="utf-8"></script>

"""


def render_template(string, context=None):
    context = context or {}
    context = Context(context)
    return Template(string).render(context)


class TestIncludeTag(unittest.TestCase):
    # Not only does this test the output of the template tag,
    # but also the order of including the static files - mainly
    # d3 and nvd3 js files which should be in that order.

    @override_settings(STATIC_URL='/static/')
    def test_custom_dirs(self):
        rendered = render_template(
            "{% load nvd3_tags %}"
            "{% include_chart_jscss css_dir='css' js_dir='js' %}"
        )
        expected = HEADER.format(css="/static/css/nv.d3.min.css",
                                 d3js="/static/js/d3.v3.min.js",
                                 nvd3js="/static/js/nv.d3.min.js")
        self.assertEqual(rendered, expected)

    @override_settings(STATIC_URL='/static/')
    def test_default_dirs(self):
        rendered = render_template(
            "{% load nvd3_tags %}"
            "{% include_chart_jscss %}"
        )
        expected = HEADER.format(css="/static/nv.d3.min.css",
                                 d3js="/static/d3.v3.min.js",
                                 nvd3js="/static/nv.d3.min.js")
        self.assertEqual(rendered, expected)


class NVD3TemplateTagsTestCase(unittest.TestCase):

    def testPiechart(self):
        xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries",
                 "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
        ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
        chartdata = {'x': xdata, 'y': ydata}
        charttype = "pieChart"
        extra = {'y_is_date': False}

        self.assertTrue(load_chart(charttype, chartdata, 'container', extra))
        self.assertTrue(include_container('container', height=400, width=600))


if __name__ == '__main__':
    unittest.main()
