"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from django.shortcuts import render
import textwrap
from django.http import HttpResponse
from api.models import Module
from api.models import Application
from api.models import Board

BOOTSTRAP_COLUMS_PER_ROW = 12
CFG_APPLICATIONS_PER_ROW = 2
CFG_MODULES_PER_ROW = 4

STATIC_PREFIX="/static/web"

def get_html(request):
    return HttpResponse(textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
            {HTML_HEADER}
            <body>
                {HEADER}
                <div class="container">
                {TABS}
                </div>
                {FOOTER}
            </body>
        </html>
    """.format(HTML_HEADER=html_header(),
               HEADER=header(),
               TABS=tabs(),
               FOOTER=footer())))


def html_header():
    """
    Get HTML code for HTML header
    Returns
    -------
    string
        HTML code
    """
    return textwrap.dedent("""
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <link rel="icon" href="{0}/img/favicon.png" type="image/png">
            <link rel="stylesheet" href="{0}/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="{0}/css/custom.css" />
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
            <script src="{0}/js/bootstrap.min.js"></script>
            <script src="{0}/js/main.js"></script>
            <script src="{0}/js/browser-integration.js"></script>
            <script src="{0}/js/dialogs.js"></script>
            <script src="{0}/js/webusb-autodetect.js"></script>

            <title>RAPstore</title>
        </head>
    """.format(STATIC_PREFIX))


def header():
    """
    Get HTML code for header
    Returns
    -------
    string
        HTML code
    """
    return textwrap.dedent("""
        <div class="jumbotron">
            <div class="container">
                <div class="row">
                    <div class="col-sm-8">
                        <h1>RAPstore</h1>
                        <p>Let us build your custom RIOT OS according to your needs</p>
                    </div>
                    <div class="col-sm-4">
                        <img src="{0}/img/riot_logo.png" alt="RIOT logo" class="img-responsive"></img>
                    </div>

                    {MODAL_DIALOG}
                </div>
            </div>
        </div>
    """.format(STATIC_PREFIX, MODAL_DIALOG=modal_dialog('modalDialogBrowserIntegration', 'Component for RAPstore browser integration is missing', '')))


def tabs():
    """
    Get HTML code for tab navigation
    Returns
    -------
    string
        HTML code
    """
    return textwrap.dedent("""
        <ul id="navigations_tabs" class="nav nav-tabs">
            <li class="active"><a data-toggle="tab" href="#tab0">Example applications</a></li>
            <li><a data-toggle="tab" href="#tab1">Your custom RIOT OS</a></li>
        </ul>
        <div class="tab-content">
            <div id="tab0" class="tab-pane fade in active">
                {EXAMPLE_TAB}
            </div>

            <div id="tab1" class="tab-pane fade">
                {CUSTOM_TAB}
            </div>

        </div>
    """.format(EXAMPLE_TAB=examples_tab("examplesTab_"),
               CUSTOM_TAB=custom_tab("customTab_")))


def custom_tab(id_prefix):
    """
    Get HTML code for custom tab
    Parameters
    ----------
    id_prefix: string
        ID prefix for the tab
    Returns
    -------
    string
        HTML code
    """
    boards = Board.objects.all()
    modules = Module.objects.all()

    board_selector_html = board_selector(id_prefix, boards)
    modules_html = module_selection(modules)

    return textwrap.dedent("""
        {BOARD_SELECTOR}
        {FILE_UPLOAD}
        {MODULES}
        <h3>4. Build and flash:</h3>
        <div class="container-fluid">
            <button type="button" class="btn btn-primary" id="{BUTTON_ID}" onclick="download()">Compile your personal RIOT OS</button>
            <div class="well" id="{CMD_OUTPUT_ID}">
                <div class="progress">
                    <div class="progress-bar progress-bar-striped active" id="{PROGRESSBAR_ID}" style="width:100%; visibility:hidden"></div>
                </div>
            </div>
        </div>
    """.format(BOARD_SELECTOR=board_selector_html,
               FILE_UPLOAD=file_upload_input(id_prefix),
               MODULES=modules_html,
               BUTTON_ID=id_prefix+"downloadButton",
               CMD_OUTPUT_ID=id_prefix+"cmdOutput",
               PROGRESSBAR_ID=id_prefix+"progressBar"))


def examples_tab(id_prefix):
    """
    Get HTML code for examples tab
    Parameters
    ----------
    id_prefix: string
        ID prefix for the tab
    Returns
    -------
    string
        HTML code
    """
    boards = Board.objects.all()
    apps = Application.objects.all()

    board_selector_html = board_selector(id_prefix, boards)
    applications_html = application_selection(id_prefix, apps)

    return textwrap.dedent("""
        {BOARD_SELECTOR}
        {APPLICATIONS}
    """.format(BOARD_SELECTOR=board_selector_html,
               APPLICATIONS=applications_html))


# https://codepen.io/CSWApps/pen/GKtvH
def file_upload_input(id_prefix):
    """
    Get HTML code for file upload input field
    Parameters
    ----------
    id_prefix: string
        ID prefix for the input field
    Returns
    -------
    string
        HTML code
    """
    return textwrap.dedent("""
        <h3>2. Upload your main C file:</h3>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-6">
                    <input id="{INPUT_ID}" type="file" name="img[]" class="file">
                    <div class="input-group">
                        <input type="text" class="form-control" readonly placeholder="Upload main source file">
                        <span class="input-group-btn">
                            <button class="browse btn btn-primary" type="button"><i class="glyphicon glyphicon-search"></i> Browse</button>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    """.format(INPUT_ID=id_prefix+"main_file_input"))


def board_selector(id_prefix, boards):
    """
    Get HTML code for board selector
    Parameters
    ----------
    id_prefix: string
        ID prefix for the selector
    boards: dict
        Fetched boards from database
    Returns
    -------
    string
        HTML code
    """
    selector_options = ''

    for board in boards:
        selector_options += '<option value="{!s}">{!s}</option>'.format(board.internal_name, board.display_name)

    return textwrap.dedent("""
        <h3>1. Select a board:</h3>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-10">
                    <div class="form-group">
                        <select class="form-control" id="{SELECTOR_ID}">
                            {SELECTOR_OPTIONS}
                        </select>
                    </div>
                </div>
                <div class="col-md-2">
                    <button id="{ID_PREFIX}autodetectButton" type="button" class="btn btn-default btn-block" onclick="autodetect('{SELECTOR_ID}')">Try autodetect</button>
                </div>
            </div>
        </div>
    """.format(ID_PREFIX=id_prefix,
               SELECTOR_ID=id_prefix+"boardSelector",
               SELECTOR_OPTIONS=selector_options))


def slices(input_list, group_size):
    """
    Cut list in to chunks of given size
    Parameters
    ----------
    input_list: list
        List to cut
    group_size: int
        Chunk size
    Returns
    -------
    array_like
        List of chunks
    """
    return [input_list[x:x + group_size] for x in range(0, len(input_list), group_size)]


def module_selection(modules, elements_per_row=CFG_MODULES_PER_ROW):
    """
    Get HTML code for module selection
    Parameters
    ----------
    modules: dict
        Fetched modules from database
    elements_per_row: int, optional
        Amount of elements per row
    Returns
    -------
    string
        HTML code
    """
    column_width = int(BOOTSTRAP_COLUMS_PER_ROW / elements_per_row)

    row_template = textwrap.dedent("""
        <div class="row">
            {COLUMNS}
        </div>
    """)

    column_template = textwrap.dedent("""
        <div class="col-md-""" + str(column_width) + """">
            <label>
                <input type="checkbox" name="module_checkbox" value="{!s}">
                <div data-toggle="tooltip" data-placement="bottom" title="{!s}">{!s}</div>
            </label>
        </div>
    """)

    checkboxes_html = ""

    checkbox_groups = {}

    for module in modules:

        group = module.group_identifier
        checkbox_groups.setdefault(group, []).append(module)

    for group, modules in sorted(checkbox_groups.items()):
        modules = sorted(modules, key=lambda x:x.name)
        checkboxes_html += '<div class="checkbox well"><h4>' + group + '</h4>'

        grouped_checkboxes_slices = slices(modules, elements_per_row)

        for grouped_checkboxes in grouped_checkboxes_slices:

            columns = ""
            for checkbox in grouped_checkboxes:
                description = checkbox.description or ""
                columns += column_template.format(checkbox.id, description, checkbox.name)

            checkboxes_html += row_template.format(COLUMNS=columns)

        checkboxes_html += '</div>'

    return textwrap.dedent("""
        <h3>3. Select modules:</h3>
        <div class="container-fluid">
            {ROWS}
        </div>
    """.format(ROWS=checkboxes_html))


def application_selection(id_prefix, apps, elements_per_row=CFG_APPLICATIONS_PER_ROW):
    """
    Get HTML code for application selector
    Parameters
    ----------
    id_prefix: string
        ID prefix als subelements within selector
    apps: dict
        Fetched applications from database
    elements_per_row: int, optional
        Amount of elements per row
    Returns
    -------
    string
        HTML code
    """
    column_width = int(BOOTSTRAP_COLUMS_PER_ROW / elements_per_row)

    row_template = textwrap.dedent("""
        <div class="row">
            {COLUMNS}
        </div>
    """)

    column_template = textwrap.dedent("""
        <div class="col-md-""" + str(column_width) + """">
            {APPLICATION_PANEL}
        </div>
    """)

    grouped_applications_slices = slices(apps, elements_per_row)

    applications_html = ""
    for grouped_applications in grouped_applications_slices:

        columns = ""
        for application in grouped_applications:

            description = application.description
            if not description:
                description = "There is no description yet"

            application_panel = collapsible_panel(application.name,
                                                  description,
                                                  application.id,
                                                  id_prefix)

            columns += column_template.format(APPLICATION_PANEL=application_panel)

        applications_html += row_template.format(COLUMNS=columns)

    return textwrap.dedent("""
        <h3>2. Select an application:</h3>
            <div class="container-fluid">
                {ROWS}
            </div>
    """.format(ROWS=applications_html))


def collapsible_panel(title, content, application_id, id_prefix):
    """
    Get HTML code for collapsible panel
    Parameters
    ----------
    title: string
        Title for the panel
    content: string
        Content text for the panel
    application_id: string
        ID of the associated application
    id_prefix: string
        ID prefix for all subelements within the panel
    Returns
    -------
    string
        HTML code
    """
    progress_div_id = id_prefix + "progressDiv" + str(application_id)
    progressbar_id = id_prefix + "progressBar" + str(application_id)
    panel_id = id_prefix + "panel" + str(application_id)
    button_id = id_prefix + "button" + str(application_id)

    modal_dialog_id = id_prefix + "modalDialog" + str(application_id)
    modal_dialog_html = modal_dialog(modal_dialog_id, "Error log", "")

    return textwrap.dedent("""
        <div id="{PANEL_ID}" class="panel panel-default">
            <div class="panel-heading">
                <h4 class="panel-title">
                    <a class="collapsed" data-toggle="collapse" data-target="#panel_body{APPLICATION_ID}" style="cursor:pointer;">{TITLE}</a>
                </h4>
            </div>
            <div id="panel_body{APPLICATION_ID}" class="panel-body collapse">
                {CONTENT}
            </div>
            <div class="panel-footer">
                <div class="row">
                    <div class="col-md-4">
                        <button id="{BUTTON_ID}" type="button" class="btn btn-primary" onclick="download_example('{APPLICATION_ID}', '{PROGRESS_DIV_ID}', '{PROGRESSBAR_ID}', '{PANEL_ID}', '{BUTTON_ID}', '{MODAL_DIALOG_ID}')">Download and flash</button>
                    </div>
                    <div class="col-md-8">
                        <div class="progress" id="{PROGRESS_DIV_ID}" style="visibility:hidden">
                            <div class="progress-bar progress-bar-striped active" id="{PROGRESSBAR_ID}" style="width:100%;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {MODAL_DIALOG}
    """.format(TITLE=title,
               CONTENT=content,
               APPLICATION_ID=application_id,
               PROGRESS_DIV_ID=progress_div_id,
               PROGRESSBAR_ID=progressbar_id,
               PANEL_ID=panel_id,
               BUTTON_ID=button_id,
               MODAL_DIALOG_ID=modal_dialog_id,
               MODAL_DIALOG=modal_dialog_html))


def modal_dialog(dialog_id, title, message):
    """
    Get HTML code for modal dialog
    Parameters
    ----------
    dialog_id: string
        ID for the dialog
    title: string
        Title for the dialog
    message: string
        Message for the dialog
    Returns
    -------
    string
        HTML code
    """
    return textwrap.dedent("""
        <div class="modal fade" id="{DIALOG_ID}" role="dialog">
            <div class="modal-dialog modal-lg">

            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <h4 class="modal-title">{TITLE}</h4>
                </div>
                <div class="modal-body">
                    {MESSAGE}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>

            </div>
        </div>
    """.format(DIALOG_ID=dialog_id,
               TITLE=title,
               MESSAGE=message))


def footer():
    """
    Get HTML code for footer
    Returns
    -------
    string
        HTML code
    """
    return textwrap.dedent("""
        <footer class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-sm-8">&copy; 2017-2018</div>
                    <div class="col-sm-4"><a href="https://riot-os.org/"><img src="{0}/img/riot_logo_footer.png" alt="RIOT logo" width="64" height="35"></img></a></div>
                </div>
            </div>
        </footer>
    """.format(STATIC_PREFIX))

