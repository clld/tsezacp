<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}">
        Tsez Annotated Corpus Project
    </a>
</%block>

${next.body()}
