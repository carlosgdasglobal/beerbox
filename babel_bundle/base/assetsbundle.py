import os

from odoo.tools import misc
from odoo.addons.base.ir.ir_qweb.assetsbundle import JavascriptAsset, rjsmin
from subprocess import Popen, PIPE

import logging
_logger = logging.getLogger(__name__)

MAX_CSS_RULES = 4095


class JavascriptAssetBabel(JavascriptAsset):
    def __init__(self, bundle, inline=None, url=None, filename=None, babel=None):
        super().__init__(bundle, inline, url, filename)
        self.babel = babel

    def minify(self):
        if self.babel:
            return self.with_header(rjsmin(self.babel_compile()))
        return super().minify()

    def get_command(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/../'
        babel_presets = ','.join([
            os.path.join(dir_path, 'node_modules', 'babel-preset-%s' % p)
            for p in ['env', 'stage-2']
        ])
        try:
            babel = misc.find_in_path('babel')
        except IOError:
            babel = 'babel'
        return [babel, self._filename, '--presets', babel_presets]

    def babel_compile(self):
        cmd = self.get_command()
        try:
            compiler = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        except Exception:
            msg = "Could not execute command %r" % cmd[0]
            _logger.error(msg)
            return ''
        result = compiler.communicate()
        if compiler.returncode:
            cmd_output = ''.join(misc.ustr(result))
            if not cmd_output:
                cmd_output = ("Process exited with return code %d\n" %
                              compiler.returncode)
            _logger.warning(cmd_output)
            return ''
        return result[0].strip().decode('utf8')
