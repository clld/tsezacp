<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%block name="head">
<style media="screen" type="text/css">

            body {
            margin: 0;
            }

            div.annot {
            overflow-x: auto;
            }

            p.tsez {
            !font-style: bold;
            font-size: 20pt;
            }
            p.eng {}
            p.rus {}

            table {
            padding-top: 8px;
            !display: none;
            border-spacing: 5px;
            border-collapse: separate;
            }

            td {
            margin: 100px;
            padding-left: 5px;
            padding-right: 5px;
            }

            tr {
            white-space: nowrap;
            }

            span.tz a {
            }

            tr.tx td {
            background-color:lightblue;
            font-weight: bold;
            }

            tr.mb td {
            background-color:#cee3eb;
            }

            tr.mb td a {
            border-bottom: 1px dashed #000080;
            text-decoration: none;
            color: black;
            }

            tr.ge td {
            background-color:#c3e7d9;
            }

            tr.ps td {
            background-color: lightgreen;
            !color: #FFF;
            }

            div.wrapper {
            overflow:auto;
            margin-bottom: 50px;
            }

            div.left {
            float: left;
            width: 20%;
            height: 100%;
            overflow: auto;
            }

            div.center {
            float: left;
            width: 60%;
            }

            div.right {
            float: right;
            width: 20%;
            height: 100%;
            overflow: auto;
            }

            div.footer {
            height: 400px;
            background-color: lightgrey;
            }

            .footer div.f_left{
            margin-left: 20%;
            float: left;
            }

            div.f_center {
            margin-left: 10%;
            float: left;
            }

            div.f_right {
            margin-left: 10%;
            margin-right: 20%;
            margin-top: 40px;
            float: left;
            }

            ul.textlinks {
            margin: 0;
            padding: 0;
            margin-top: 30px;
            list-style-type: none;
            }

            ul.textlinks li {
            margin-top: 8px;
            list-style-type: none;
            }

            .nav {
            padding-top: 20px;
            padding-bottom: 20px;
            }
            </style>
</%block>

<h2>${ctx.name}: ${ctx.description}</h2>

% for line in ctx.lines:
<div id="l${line.id}">
    <h3 class="tsez">
        ${str(line.ord)}. ${line.name}
        <a href="#top" title="go to top of the page" style="vertical-align: bottom">&#x21eb;</a>
        <a class="headerlink" href="#l${line.id}" title="Permalink to this headline">¶</a>
    </h3>
    <div class="annot">
        <table frame="border" border="0">
            <tr class="tx">
            % for word in line.words:
                <td colspan="${len(word.morphemes)}">${word.name}</td>
            % endfor
            </tr>
            <tr class="mb">
                % for word in line.words:
                    % for morpheme in word.morphemes:
                        % if morpheme.morpheme:
                            <td>${h.link(request, morpheme.morpheme, label=morpheme.name)}</td>
                        % else:
                            <td>${morpheme.name}</td>
                        % endif
                    % endfor
                % endfor
            </tr>
            <tr class="ge">
                % for word in line.words:
                    % for morpheme in word.morphemes:
                        <td>${morpheme.description}</td>
                    % endfor
                % endfor
            </tr>
            <tr class="ps">
                % for word in line.words:
                    % for morpheme in word.morphemes:
                        <td><i>${morpheme.pos}</i></td>
                    % endfor
                % endfor
            </tr>
        </table>
    </div>
    <br/>
    <p class="eng">${line.description}</p>
    <p class="rus">${line.russian}</p>
    <hr size="2" color="orange"/>
</div>
% endfor
