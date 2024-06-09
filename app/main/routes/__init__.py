# app/main/routes/__init__.py

from flask import Blueprint

from .. import main
from . import confirmation, customer_info, error_handlers, reserve, search, thank_you


def register_blueprints(main_blueprint):
    main_blueprint.register_blueprint(search.bp)
    main_blueprint.register_blueprint(reserve.bp)
    main_blueprint.register_blueprint(customer_info.bp)
    main_blueprint.register_blueprint(confirmation.bp)
    main_blueprint.register_blueprint(thank_you.bp)
    main_blueprint.register_blueprint(error_handlers.bp)


register_blueprints(main)
