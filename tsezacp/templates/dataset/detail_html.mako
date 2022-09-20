<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>How to cite</h3>
        <p>If you use this data please cite</p>
        <blockquote>${req.dataset.jsondata['data_citation']}</blockquote>
        <p>as well as the original source</p>
        <blockquote>${req.dataset.jsondata['source_citation']}</blockquote>
    </div>
</%def>

<h2>${req.dataset.name}</h2>
${req.dataset.description|n}
<p>
    Questions, corrections, suggestions for improvements, etc. should be addressed
    to Bernard Comrie at comrie@linguistics.ucsb.edu.
</p>
