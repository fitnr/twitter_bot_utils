from . import api as API

def no_entities(status):
    try:
        e = status.entities
    except AttributeError:
        return True
    if len(e['urls']) == 0 and len(e['hashtags']) == 0 and len(e['user_mentions']) == 0:
        return True
    else:
        return False

def clean_status(status):
    try:
        if no_entities(status) and status.metadata.get('iso_language_code') == 'en':
            return True
        else:
            return False
    except AttributeError:
        return False

def format_status(status):
    return status.text.replace(u'&amp;', u'&').replace('&lt;', '<').replace('&gt;', '>').replace('\n', ' ')


def follow_back(api=False, **args):
    autofollow('follow', api, **args)


def unfollow(api=False, **args):
    autofollow('unfollow', api, **args)


def autofollow(action, api=False, **args):
    ignore = []

    try:
        api = API.check_api(api, **args)
    except Exception, e:
        raise e

    # get the last 5000 followers
    try:
        followers = api.follower_ids()
        followers = [x.id_str for x in followers]

    except Exception, e:
        raise e

    # Get the last 5000 people user has followed
    try:
        friends = api.friend_ids()

    except Exception, e:
        raise e

    if action is "unfollow":
        method = api.destroy_friendship
        independent, dependent = followers, friends

    elif action is "follow":
        method = api.create_friendship
        independent, dependent = friends, followers

    try:
        outgoing = api.friendships_outgoing()
        ignore = [x.id_str for x in outgoing]

    except Exception, e:
        raise e

    for uid in dependent:
        if uid in independent and uid not in ignore:
            try:
                method(id=uid)

            except Exception, e:
                raise e


def fave_mentions(api=False, **args):
    try:
        api = API.check_api(api, **args)
        print api.auth.get_username()
    except Exception, e:
        raise e

    favs = api.favorites(include_entities=False, count=100)
    favs = [m.id_str for m in favs]
    faved = []

    try:
        mentions = api.mentions_timeline(trim_user=True, include_entities=False, count=75)
    except Exception, e:
        raise e

    for mention in mentions:
        # only try to fav if not in recent favs
        if mention.id_str not in favs:
            try:
                fav = api.create_favorite(mention.id_str, include_entities=False)
                faved.append(fav)

            except Exception, e:
                raise e
