from app import create_app, db
import click

app = create_app()


@app.cli.command()
@click.option('--name', prompt='Organization name', help='Organization name')
def create_orga(name):
    with app.app_context():
        from app.api.organization import Organization 

        """Create organization"""
        orga = Organization()

        orga.name = name

        db.session.add(orga)
        db.session.commit()

        click.echo('Organization {} created'.format(name))


@app.cli.command()
@click.option('--email', prompt='Your email', help='User email')
@click.password_option('--password', prompt='Type password', help='User password')
@click.option('--name', help='User name')
@click.option('--surname', help='User suername')
@click.option('--admin',  is_flag=True,
              help='Flag to indicate user is admin', )
@click.option('--organization', default=1, help='Organization to associate user (Default: 1)')
def create_user(email, password, name, surname, admin, organization):
    with app.app_context():
        from app.api.user import User
        from datetime import datetime

        """Create user"""
        user = User()

        user.email = email
        user.is_superadmin = admin  # TODO: Remove superadmin RoleNeed when permissions active
        user.encode_password(password)
        user.id_organization = organization

        user.name = name
        user.surname = surname

        user.registered_on = datetime.now()

        db.session.add(user)

        db.session.commit()

        click.echo('User {} created in organization {}'.format(email, organization))


@app.shell_context_processor
def make_shell_context():
    return {'db': db}
