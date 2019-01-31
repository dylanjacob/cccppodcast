
import unittest

from flask.cli import FlaskGroup

from lib import create_app, db
from lib.api.models import Episode

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    """Recreate the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Run the tests without code coverage."""
    tests = unittest.TestLoader().discover('lib/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    """Seed the database with test data."""
    db.session.add(Episode(title='A Test Episode',
                           summary='Lorem ipsum dolor sit amet.',
                           media='https://localhost/buckets/0123456/file.mp3'))
    db.session.add(Episode(title='Another Test Episode',
                           summary='Lorem ipsum dolor sit amet.',
                           media='https://localhost/buckets/6543210/file.mp3'))
    db.session.commit()


if __name__ == '__main__':
    cli()
