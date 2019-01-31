import json
import unittest

from lib import db
from lib.api.models import Episode
from lib.tests.base import BaseTestCase


def add_episode(title, summary, media):
    episode = Episode(title=title, summary=summary, media=media)
    db.session.add(episode)
    db.session.commit()
    return episode


class TestRSSService(BaseTestCase):
    """Test the RSS service."""

    def test_rss(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/episodes/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_episode(self):
        """Ensure a new episode can be added to the database."""
        with self.client:
            response = self.client.post(
                '/episodes',
                data=json.dumps({
                    'title': 'A Test Episode',
                    'summary': 'Lorem ipsum dolor sit amet.',
                    'media': 'https://localhost/buckets/0123456/file.mp3'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('A Test Episode was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_episode_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/episodes',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_episode_invalid_json_keys(self):
        """Ensure error is thrown if the JSON doesn't have a title key."""
        with self.client:
            response = self.client.post(
                '/episodes',
                data=json.dumps({'summary': 'Lorem ipsum dolor sit amet.'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_episode_duplicate_email(self):
        """Ensure error is thrown if the title already exists."""
        with self.client:
            self.client.post(
                '/episodes',
                data=json.dumps({
                    'title': 'A Test Episode',
                    'summary': 'Lorem ipsum dolor sit amet.',
                    'media': 'https://localhost/buckets/0123456/file.mp3'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/episodes',
                data=json.dumps({
                    'title': 'A Test Episode',
                    'summary': 'Lorem ipsum dolor sit amet.',
                    'media': 'https://localhost/buckets/0123456/file.mp3'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry, that episode already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_episode(self):
        """Ensure get single episode behaves correctly."""
        episode = add_episode('A Test Episode', 'Lorem ipsum dolor sit amet.',
                              'https://localhost/buckets/0123456/file.mp3')
        with self.client:
            response = self.client.get(f'/episodes/{episode.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('A Test Episode', data['data']['title'])
            self.assertIn('Lorem ipsum dolor sit amet.',
                          data['data']['summary'])
            self.assertIn('https://localhost/buckets/0123456/file.mp3',
                          data['data']['media'])
            self.assertIn('success', data['status'])

    def test_single_episode_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/episodes/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Episode does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_episode_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/episodes/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Episode does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_episodes(self):
        """Ensure get all episodes behaves correctly."""
        add_episode('A Test Episode',
                    'Lorem ipsum dolor sit amet.',
                    'https://localhost/buckets/0123456/file.mp3')
        add_episode('Another Test Episode',
                    'Lorem ipsum dolor sit amet.',
                    'https://localhost/buckets/6543210/file.mp3')
        with self.client:
            response = self.client.get('/episodes')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['episodes']), 2)
            self.assertIn('A Test Episode',
                          data['data']['episodes'][0]['title'])
            self.assertIn('Lorem ipsum dolor sit amet.',
                          data['data']['episodes'][0]['summary'])
            self.assertIn('https://localhost/buckets/0123456/file.mp3',
                          data['data']['episodes'][0]['media'])
            self.assertIn('Another Test Episode',
                          data['data']['episodes'][1]['title'])
            self.assertIn('Lorem ipsum dolor sit amet.',
                          data['data']['episodes'][1]['summary'])
            self.assertIn('https://localhost/buckets/6543210/file.mp3',
                          data['data']['episodes'][1]['media'])
            self.assertIn('success', data['status'])

    def test_main_no_episodes(self):
        """Ensure the main route behaves correctly when no episodes have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Episodes', response.data)
        self.assertIn(b'<p>No episodes!</p>', response.data)

    def test_main_with_episodes(self):
        """Ensure the main route behaves correctly when episodes have been
        added to the database."""
        add_episode('A Test Episode',
                    'Lorem ipsum dolor sit amet.',
                    'https://localhost/buckets/0123456/file.mp3')
        add_episode('Another Test Episode',
                    'Lorem ipsum dolor sit amet.',
                    'https://localhost/buckets/6543210/file.mp3')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Episodes', response.data)
            self.assertNotIn(b'<p>No episodes!</p>', response.data)
            self.assertIn(b'A Test Episode', response.data)
            self.assertIn(b'Another Test Episode', response.data)

    def test_main_add_user(self):
        """Ensure a new episode can be added to the db via POST request."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(title='A Test Episode',
                          summary='Lorem ipsum dolor sit amet.',
                          media='https://localhost/buckets/0123456/file.mp3'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Episodes', response.data)
            self.assertNotIn(b'<p>No episodes!</p>', response.data)
            self.assertIn(b'A Test Episode', response.data)

if __name__ == '__main__':
    unittest.main()
