"""
This type stub file was generated by pyright.
"""

from .helpers import _PackageBoundObject
from typing import Any, Optional

"""
    flask.blueprints
    ~~~~~~~~~~~~~~~~

    Blueprints are the recommended way to implement larger or more
    pluggable applications in Flask 0.7 and later.

    :copyright: 2010 Pallets
    :license: BSD-3-Clause
"""
_sentinel = object()
class BlueprintSetupState(object):
    """Temporary holder object for registering a blueprint with the
    application.  An instance of this class is created by the
    :meth:`~flask.Blueprint.make_setup_state` method and later passed
    to all register callback functions.
    """
    def __init__(self, blueprint, app, options, first_registration):
        self.app = ...
        self.blueprint = ...
        self.options = ...
        self.first_registration = ...
        self.subdomain = ...
        self.url_prefix = ...
        self.url_defaults = ...
    
    def add_url_rule(self, rule, endpoint: Optional[Any] = ..., view_func: Optional[Any] = ..., **options):
        """A helper method to register a rule (and optionally a view function)
        to the application.  The endpoint is automatically prefixed with the
        blueprint's name.
        """
        ...
    


class Blueprint(_PackageBoundObject):
    """Represents a blueprint, a collection of routes and other
    app-related functions that can be registered on a real application
    later.

    A blueprint is an object that allows defining application functions
    without requiring an application object ahead of time. It uses the
    same decorators as :class:`~flask.Flask`, but defers the need for an
    application by recording them for later registration.

    Decorating a function with a blueprint creates a deferred function
    that is called with :class:`~flask.blueprints.BlueprintSetupState`
    when the blueprint is registered on an application.

    See :ref:`blueprints` for more information.

    .. versionchanged:: 1.1.0
        Blueprints have a ``cli`` group to register nested CLI commands.
        The ``cli_group`` parameter controls the name of the group under
        the ``flask`` command.

    .. versionadded:: 0.7

    :param name: The name of the blueprint. Will be prepended to each
        endpoint name.
    :param import_name: The name of the blueprint package, usually
        ``__name__``. This helps locate the ``root_path`` for the
        blueprint.
    :param static_folder: A folder with static files that should be
        served by the blueprint's static route. The path is relative to
        the blueprint's root path. Blueprint static files are disabled
        by default.
    :param static_url_path: The url to serve static files from.
        Defaults to ``static_folder``. If the blueprint does not have
        a ``url_prefix``, the app's static route will take precedence,
        and the blueprint's static files won't be accessible.
    :param template_folder: A folder with templates that should be added
        to the app's template search path. The path is relative to the
        blueprint's root path. Blueprint templates are disabled by
        default. Blueprint templates have a lower precedence than those
        in the app's templates folder.
    :param url_prefix: A path to prepend to all of the blueprint's URLs,
        to make them distinct from the rest of the app's routes.
    :param subdomain: A subdomain that blueprint routes will match on by
        default.
    :param url_defaults: A dict of default values that blueprint routes
        will receive by default.
    :param root_path: By default, the blueprint will automatically this
        based on ``import_name``. In certain situations this automatic
        detection can fail, so the path can be specified manually
        instead.
    """
    warn_on_modifications = ...
    _got_registered_once = ...
    json_encoder = ...
    json_decoder = ...
    import_name = ...
    template_folder = ...
    root_path = ...
    def __init__(self, name, import_name, static_folder: Optional[Any] = ..., static_url_path: Optional[Any] = ..., template_folder: Optional[Any] = ..., url_prefix: Optional[Any] = ..., subdomain: Optional[Any] = ..., url_defaults: Optional[Any] = ..., root_path: Optional[Any] = ..., cli_group=...):
        self.name = ...
        self.url_prefix = ...
        self.subdomain = ...
        self.static_folder = ...
        self.static_url_path = ...
        self.deferred_functions = ...
        self.url_values_defaults = ...
        self.cli_group = ...
    
    def record(self, func):
        """Registers a function that is called when the blueprint is
        registered on the application.  This function is called with the
        state as argument as returned by the :meth:`make_setup_state`
        method.
        """
        ...
    
    def record_once(self, func):
        """Works like :meth:`record` but wraps the function in another
        function that will ensure the function is only called once.  If the
        blueprint is registered a second time on the application, the
        function passed is not called.
        """
        ...
    
    def make_setup_state(self, app, options, first_registration: bool = ...):
        """Creates an instance of :meth:`~flask.blueprints.BlueprintSetupState`
        object that is later passed to the register callback functions.
        Subclasses can override this to return a subclass of the setup state.
        """
        ...
    
    def register(self, app, options, first_registration: bool = ...):
        """Called by :meth:`Flask.register_blueprint` to register all views
        and callbacks registered on the blueprint with the application. Creates
        a :class:`.BlueprintSetupState` and calls each :meth:`record` callback
        with it.

        :param app: The application this blueprint is being registered with.
        :param options: Keyword arguments forwarded from
            :meth:`~Flask.register_blueprint`.
        :param first_registration: Whether this is the first time this
            blueprint has been registered on the application.
        """
        ...
    
    def route(self, rule, **options):
        """Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
        :func:`url_for` function is prefixed with the name of the blueprint.
        """
        ...
    
    def add_url_rule(self, rule, endpoint: Optional[Any] = ..., view_func: Optional[Any] = ..., **options):
        """Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
        the :func:`url_for` function is prefixed with the name of the blueprint.
        """
        ...
    
    def endpoint(self, endpoint):
        """Like :meth:`Flask.endpoint` but for a blueprint.  This does not
        prefix the endpoint with the blueprint name, this has to be done
        explicitly by the user of this method.  If the endpoint is prefixed
        with a `.` it will be registered to the current blueprint, otherwise
        it's an application independent endpoint.
        """
        ...
    
    def app_template_filter(self, name: Optional[Any] = ...):
        """Register a custom template filter, available application wide.  Like
        :meth:`Flask.template_filter` but for a blueprint.

        :param name: the optional name of the filter, otherwise the
                     function name will be used.
        """
        ...
    
    def add_app_template_filter(self, f, name: Optional[Any] = ...):
        """Register a custom template filter, available application wide.  Like
        :meth:`Flask.add_template_filter` but for a blueprint.  Works exactly
        like the :meth:`app_template_filter` decorator.

        :param name: the optional name of the filter, otherwise the
                     function name will be used.
        """
        ...
    
    def app_template_test(self, name: Optional[Any] = ...):
        """Register a custom template test, available application wide.  Like
        :meth:`Flask.template_test` but for a blueprint.

        .. versionadded:: 0.10

        :param name: the optional name of the test, otherwise the
                     function name will be used.
        """
        ...
    
    def add_app_template_test(self, f, name: Optional[Any] = ...):
        """Register a custom template test, available application wide.  Like
        :meth:`Flask.add_template_test` but for a blueprint.  Works exactly
        like the :meth:`app_template_test` decorator.

        .. versionadded:: 0.10

        :param name: the optional name of the test, otherwise the
                     function name will be used.
        """
        ...
    
    def app_template_global(self, name: Optional[Any] = ...):
        """Register a custom template global, available application wide.  Like
        :meth:`Flask.template_global` but for a blueprint.

        .. versionadded:: 0.10

        :param name: the optional name of the global, otherwise the
                     function name will be used.
        """
        ...
    
    def add_app_template_global(self, f, name: Optional[Any] = ...):
        """Register a custom template global, available application wide.  Like
        :meth:`Flask.add_template_global` but for a blueprint.  Works exactly
        like the :meth:`app_template_global` decorator.

        .. versionadded:: 0.10

        :param name: the optional name of the global, otherwise the
                     function name will be used.
        """
        ...
    
    def before_request(self, f):
        """Like :meth:`Flask.before_request` but for a blueprint.  This function
        is only executed before each request that is handled by a function of
        that blueprint.
        """
        ...
    
    def before_app_request(self, f):
        """Like :meth:`Flask.before_request`.  Such a function is executed
        before each request, even if outside of a blueprint.
        """
        ...
    
    def before_app_first_request(self, f):
        """Like :meth:`Flask.before_first_request`.  Such a function is
        executed before the first request to the application.
        """
        ...
    
    def after_request(self, f):
        """Like :meth:`Flask.after_request` but for a blueprint.  This function
        is only executed after each request that is handled by a function of
        that blueprint.
        """
        ...
    
    def after_app_request(self, f):
        """Like :meth:`Flask.after_request` but for a blueprint.  Such a function
        is executed after each request, even if outside of the blueprint.
        """
        ...
    
    def teardown_request(self, f):
        """Like :meth:`Flask.teardown_request` but for a blueprint.  This
        function is only executed when tearing down requests handled by a
        function of that blueprint.  Teardown request functions are executed
        when the request context is popped, even when no actual request was
        performed.
        """
        ...
    
    def teardown_app_request(self, f):
        """Like :meth:`Flask.teardown_request` but for a blueprint.  Such a
        function is executed when tearing down each request, even if outside of
        the blueprint.
        """
        ...
    
    def context_processor(self, f):
        """Like :meth:`Flask.context_processor` but for a blueprint.  This
        function is only executed for requests handled by a blueprint.
        """
        ...
    
    def app_context_processor(self, f):
        """Like :meth:`Flask.context_processor` but for a blueprint.  Such a
        function is executed each request, even if outside of the blueprint.
        """
        ...
    
    def app_errorhandler(self, code):
        """Like :meth:`Flask.errorhandler` but for a blueprint.  This
        handler is used for all requests, even if outside of the blueprint.
        """
        ...
    
    def url_value_preprocessor(self, f):
        """Registers a function as URL value preprocessor for this
        blueprint.  It's called before the view functions are called and
        can modify the url values provided.
        """
        ...
    
    def url_defaults(self, f):
        """Callback function for URL defaults for this blueprint.  It's called
        with the endpoint and values and should update the values passed
        in place.
        """
        ...
    
    def app_url_value_preprocessor(self, f):
        """Same as :meth:`url_value_preprocessor` but application wide.
        """
        ...
    
    def app_url_defaults(self, f):
        """Same as :meth:`url_defaults` but application wide.
        """
        ...
    
    def errorhandler(self, code_or_exception):
        """Registers an error handler that becomes active for this blueprint
        only.  Please be aware that routing does not happen local to a
        blueprint so an error handler for 404 usually is not handled by
        a blueprint unless it is caused inside a view function.  Another
        special case is the 500 internal server error which is always looked
        up from the application.

        Otherwise works as the :meth:`~flask.Flask.errorhandler` decorator
        of the :class:`~flask.Flask` object.
        """
        ...
    
    def register_error_handler(self, code_or_exception, f):
        """Non-decorator version of the :meth:`errorhandler` error attach
        function, akin to the :meth:`~flask.Flask.register_error_handler`
        application-wide function of the :class:`~flask.Flask` object but
        for error handlers limited to this blueprint.

        .. versionadded:: 0.11
        """
        ...
    


