import api as API


def check_api(api, **args):
    if api is False:
        if args.get('screen_name') and args.get('app'):
            api = API.create(args['app'], args['screen_name'])
        else:
            raise Exception('cannot create API')
    return api


def follow_back(api=False, **args):
    autofollow('follow', api, **args)


def unfollow(api=False, **args):
    autofollow('unfollow', api, **args)


def autofollow(action, api=False, **args):
    users, ids, ignore = [], [], []

    try:
        api = check_api(api, **args)
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
        api = check_api(api, **args)
    except Exception, e:
        raise e

    favs = api.favorites(include_entities=False)
    faved = []

    try:
        mentions = api.mentions(trim_user=True, include_entities=False)
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
