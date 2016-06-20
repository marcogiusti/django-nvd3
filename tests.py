import unittest

from django.conf import settings
settings.configure(INSTALLED_APPS=["django_nvd3"])
import django
django.setup()
from django.template import Context, Template
from django.test.utils import override_settings
from django_nvd3.templatetags.nvd3_tags import load_chart, include_container


class NVD3TemplateTagsTestCase(unittest.TestCase):

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def testPiechart(self):
        xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries",
                 "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
        ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
        chartdata = {'x': xdata, 'y': ydata}
        charttype = "pieChart"
        extra = {'y_is_date': False}

        self.assertTrue(load_chart(charttype, chartdata, 'container', extra))
        self.assertTrue(include_container('container', height=400, width=600))

    @override_settings(STATIC_URL='/static/')
    def test_include_chart_jscss_tag_custom_dirs(self):
        rendered = self.render_template(
            "{% load nvd3_tags %}"
            "{% include_chart_jscss css_dir='css' js_dir='js' %}"
        )

        # Not only does this test the output of the template tag,
        # but also the order of including the static files - mainly
        # d3 and nvd3 js files which should be in that order.
        expected = (
            '<link media="all" href="/static/css/nv.d3.min.css" '
            'type="text/css" rel="stylesheet" />\n'
            '<script src="/static/js/d3.min.js" '
            'type="text/javascript" charset="utf-8"></script>\n'
            '<script src="/static/js/nv.d3.min.js" '
            'type="text/javascript" charset="utf-8"></script>\n\n'
        )
        self.assertEqual(rendered, expected)


if __name__ == '__main__':
    unittest.main()
