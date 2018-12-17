import json
import logging

from lxml import html
from werkzeug import urls

from odoo.tools import pycompat

from odoo import models, tools
from odoo.http import request
from odoo.modules.module import get_resource_path

from odoo.addons.base.ir.ir_qweb.qweb import QWeb

_logger = logging.getLogger(__name__)


class IrQwebBabel(models.AbstractModel, QWeb):

    _inherit = 'ir.qweb'

    @tools.ormcache_context('xmlid', 'options.get("lang", "en_US")',
                            keys=("website_id",))
    def _get_asset_content(self, xmlid, options):
        options = dict(options,
                       inherit_branding=False, inherit_branding_auto=False,
                       edit_translations=False, translatable=False,
                       rendering_bundle=True)

        env = self.env(context=options)

        def get_modules_order():
            if request:
                from odoo.addons.web.controllers.main import module_boot
                return json.dumps(module_boot())
            return '[]'

        template = env['ir.qweb'].render(xmlid, {
            "get_modules_order": get_modules_order})

        files = []
        remains = []
        for el in html.fragments_fromstring(template):
            if isinstance(el, pycompat.string_types):
                remains.append(pycompat.to_text(el))
            elif isinstance(el, html.HtmlElement):
                href = el.get('href', '')
                src = el.get('src', '')
                atype = el.get('type')
                media = el.get('media')

                can_aggregate = not urls.url_parse(
                    href).netloc and not href.startswith('/web/content')
                if el.tag == 'style' or (el.tag == 'link' and el.get(
                        'rel') == 'stylesheet' and can_aggregate):
                    if href.endswith('.sass'):
                        atype = 'text/sass'
                    elif href.endswith('.less'):
                        atype = 'text/less'
                    if atype not in ('text/less', 'text/sass'):
                        atype = 'text/css'
                    path = [segment for segment in href.split('/') if segment]
                    filename = get_resource_path(*path) if path else None
                    files.append(
                        {'atype': atype, 'url': href, 'filename': filename,
                         'content': el.text, 'media': media})
                elif el.tag == 'script':
                    atype = 'text/javascript'
                    babel = el.get('babel')
                    path = [segment for segment in src.split('/') if segment]
                    filename = get_resource_path(*path) if path else None
                    files.append(
                        {'atype': atype, 'url': src, 'filename': filename,
                         'content': el.text, 'media': media, 'babel': babel})
                else:
                    remains.append(html.tostring(el, encoding='unicode'))
            else:
                try:
                    remains.append(html.tostring(el, encoding='unicode'))
                except Exception:
                    # notYETimplementederror
                    raise NotImplementedError

        return (files, remains)