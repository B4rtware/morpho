"""
This type stub file was generated by pyright.
"""

import logging
import click
from clickclick import AliasedGroup

logger = logging.getLogger('connexion.cli')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
FLASK_APP = 'flask'
AIOHTTP_APP = 'aiohttp'
AVAILABLE_SERVERS = { 'flask': [FLASK_APP],'gevent': [FLASK_APP],'tornado': [FLASK_APP],'aiohttp': [AIOHTTP_APP] }
AVAILABLE_APPS = { FLASK_APP: 'connexion.apps.flask_app.FlaskApp',AIOHTTP_APP: 'connexion.apps.aiohttp_app.AioHttpApp' }
DEFAULT_SERVERS = { FLASK_APP: FLASK_APP,AIOHTTP_APP: AIOHTTP_APP }
def validate_server_requirements(ctx, param, value):
    ...

def print_version(ctx, param, value):
    ...

@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True, help='Print the current version number and exit.')
def main():
    ...

@main.command()
@click.argument('spec_file')
@click.argument('base_module_path', required=False)
@click.option('--port', '-p', default=5000, type=int, help='Port to listen.')
@click.option('--host', '-H', type=str, help='Host interface to bind on.')
@click.option('--wsgi-server', '-w', type=click.Choice(AVAILABLE_SERVERS.keys()), callback=validate_server_requirements, help='Which WSGI server container to use. (deprecated, use --server instead)')
@click.option('--server', '-s', type=click.Choice(AVAILABLE_SERVERS.keys()), callback=validate_server_requirements, help='Which server container to use.')
@click.option('--stub', help='Returns status code 501, and `Not Implemented Yet` payload, for ' 'the endpoints which handlers are not found.', is_flag=True, default=False)
@click.option('--mock', type=click.Choice(['all', 'notimplemented']), help='Returns example data for all endpoints or for which handlers are not found.')
@click.option('--hide-spec', help='Hides the API spec in JSON format which is by default available at `/swagger.json`.', is_flag=True, default=False)
@click.option('--hide-console-ui', help='Hides the the API console UI which is by default available at `/ui`.', is_flag=True, default=False)
@click.option('--console-ui-url', metavar='URL', help='Personalize what URL path the API console UI will be mounted.')
@click.option('--console-ui-from', metavar='PATH', help='Path to a customized API console UI dashboard.')
@click.option('--auth-all-paths', help='Enable authentication to paths not defined in the spec.', is_flag=True, default=False)
@click.option('--validate-responses', help='Enable validation of response values from operation handlers.', is_flag=True, default=False)
@click.option('--strict-validation', help='Enable strict validation of request payloads.', is_flag=True, default=False)
@click.option('--debug', '-d', help='Show debugging information.', is_flag=True, default=False)
@click.option('--verbose', '-v', help='Show verbose information.', count=True)
@click.option('--base-path', metavar='PATH', help='Override the basePath in the API spec.')
@click.option('--app-framework', '-f', default=FLASK_APP, type=click.Choice(AVAILABLE_APPS.keys()), help='The app framework used to run the server')
def run(spec_file, base_module_path, port, host, wsgi_server, server, stub, mock, hide_spec, hide_console_ui, console_ui_url, console_ui_from, auth_all_paths, validate_responses, strict_validation, debug, verbose, base_path, app_framework):
    """
    Runs a server compliant with a OpenAPI/Swagger 2.0 Specification file.

    Arguments:

    - SPEC_FILE: specification file that describes the server endpoints.

    - BASE_MODULE_PATH (optional): filesystem path where the API endpoints handlers are going to be imported from.
    """
    ...

if __name__ == '__main__':
    ...
