<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "units" %>


<h2>Glossary Entry</h2>

${util.dl_table(value=ctx.name, gloss=ctx.description, part_of_speech=ctx.pos)}

% if ctx.notes:
<strong>Notes:</strong>
<p>${ctx.notes}</p>
% endif

<h3>Concordance</h3>
<%util:table items="${ctx.occurrences}" args="item">
    <%def name="head()">
        <th>Morpheme</th>
        ##<th>Line</th>
        <th>Text</th>
    </%def>
    <td>${item.name}</td>
    ##<td>${h.link(request, item.word.line)}</td>
    <td>${h.link(request, item.word.line.text, url_kw=dict(_anchor='l' + item.word.line.id))}</td>
</%util:table>