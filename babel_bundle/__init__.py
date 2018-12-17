from . import base
import odoo


def babel_patch():
    from odoo.http import request
    from odoo.addons.base.ir.ir_qweb.assetsbundle import AssetsBundle, \
        SassStylesheetAsset, LessStylesheetAsset, StylesheetAsset

    def __init__(self, name, files, remains, env=None):
        self.name = name
        self.env = request.env if env is None else env
        self.max_css_rules = self.env.context.get(
            'max_css_rules', base.assetsbundle.MAX_CSS_RULES)
        self.javascripts = []
        self.stylesheets = []
        self.css_errors = []
        self.remains = []
        self._checksum = None
        self.files = files
        self.remains = remains
        for f in files:
            if f['atype'] == 'text/sass':
                self.stylesheets.append(
                    SassStylesheetAsset(self, url=f['url'],
                                        filename=f['filename'],
                                        inline=f['content'], media=f['media']))
            elif f['atype'] == 'text/less':
                self.stylesheets.append(
                    LessStylesheetAsset(self, url=f['url'],
                                        filename=f['filename'],
                                        inline=f['content'], media=f['media']))
            elif f['atype'] == 'text/css':
                self.stylesheets.append(
                    StylesheetAsset(self, url=f['url'], filename=f['filename'],
                                    inline=f['content'], media=f['media']))
            elif f['atype'] == 'text/javascript':
                self.javascripts.append(
                    base.assetsbundle.JavascriptAssetBabel(
                        self, url=f['url'], filename=f['filename'],
                        inline=f['content'], babel=f['babel']))

    setattr(AssetsBundle, '__init__', __init__)


def uninstall_hook(cr, registry):
    odoo.service.server.restart()
