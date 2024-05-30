from flask import render_template

def register_error_handlers(app, db):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Log the error
        app.logger.error(f"Error: {str(e)}")

        if app.config['DEBUG']:
            # Show detailed error in development
            return render_template('500.html', error=str(e)), 500
        else:
            # Show generic error in production
            return render_template('500.html'), 500
