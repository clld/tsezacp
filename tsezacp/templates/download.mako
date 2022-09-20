<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>

<h3>${_('Downloads')}</h3>

<div class="alert alert-info">
    <p>
        This web application serves the latest
        ${h.external_link('https://github.com/cldf-datasets/tsezacp/releases', label=_('released version'))}
        of data curated at
        ${h.external_link('https://github.com/cldf-datasets/tsezacp', label='cldf-datasets/tsezacp')}.
        All released version are accessible via
        <a href="https://doi.org/10.5281/zenodo.7096349">DOI: 10.5281/zenodo.7096349</a>
        on ZENODO as well.
    </p>
</div>
