Compile JS Bundles via Babel 6.x.
=================================

Instruction
-----------

  1. Install babel-cli global: :code:`npm install -g babel-cli`.
  2. Add :code:`babel='True'` tag to your js assets.

Presets
-------

  - env
  - stage-2

Example
-------

::

  <template id="my_assets_frontend_js" inherit_id="website.assets_frontend">
    <xpath expr="//script[last()]" position="after">
      <script src="/website_my_addons/static/lib/history.min.js" type="text/javascript"/>
      <script src="/website_my_addons/static/lib/es6-awesome.js" type="text/javascript" babel="True"/>
    </xpath>
  </template>
