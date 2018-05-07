from app import create_app, db
import click

app = create_app()


@app.cli.command()
@click.option('--email', prompt='Your email')
@click.password_option('--password', prompt='Type password')
@click.option('--name')
@click.option('--surname')
@click.option('--admin',  is_flag=True,
              help='Indicates if user is admin', )
@click.option('--organization', default=1)
def create_user(email, password, name, surname, admin, organization):
    with app.app_context():
        from app.api.user import User
        from datetime import datetime

        """Create user"""
        admin_user = User()

        admin_user.email = email
        admin_user.is_superadmin = admin
        admin_user.encode_password(password)
        admin_user.id_organization = organization

        admin_user.name = name
        admin_user.surname = surname

        admin_user.registered_on = datetime.now()

        db.session.add(admin_user)

        db.session.commit()

        click.echo('User {} created in organization {}'.format(email, organization))


@app.shell_context_processor
def make_shell_context():
    return {'db': db}