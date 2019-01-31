# services/rsspy/lib/api/episodes.py


from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from lib.api.models import Episode
from lib import db


episodes_blueprint = Blueprint('episodes', __name__, template_folder='./templates')


@episodes_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        media = request.form['media']
        db.session.add(Episode(title=title, summary=summary, media=media))
        db.session.commit()
    episodes = Episode.query.all()
    return render_template('index.html', episodes=episodes)


@episodes_blueprint.route('/episodes/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@episodes_blueprint.route('/episodes', methods=['POST'])
def add_episode():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    title = post_data.get('title')
    summary = post_data.get('summary')
    media = post_data.get('media')
    try:
        episode = Episode.query.filter_by(title=title).first()
        if not episode:
            db.session.add(Episode(title=title, summary=summary, media=media))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{title} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry, that episode already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@episodes_blueprint.route('/episodes/<episode_id>', methods=['GET'])
def get_single_episode(episode_id):
    """Get single episode details."""
    response_object = {
        'status': 'fail',
        'message': 'Episode does not exist.'
    }
    try:
        episode = Episode.query.filter_by(id=int(episode_id)).first()
        if not episode:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': episode.id,
                    'title': episode.title,
                    'summary': episode.summary,
                    'media': episode.media,
                    'active': episode.active,
                    'created_date': episode.created_date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@episodes_blueprint.route('/episodes', methods=['GET'])
def get_all_episodes():
    """Get all episodes."""
    response_object = {
        'status': 'success',
        'data': {
            'episodes': [episode.to_json() for episode in Episode.query.all()]
        }
    }
    return jsonify(response_object), 200
