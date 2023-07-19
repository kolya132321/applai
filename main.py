from linkedin_api import Linkedin
import os
import json
from linkedin_api.utils.helpers import (
    append_update_post_field_to_posts_list,
    get_id_from_urn,
    get_list_posts_sorted_without_promoted,
    get_update_author_name,
    get_update_author_profile,
    get_update_content,
    get_update_old,
    get_update_url,
    parse_list_raw_posts,
    parse_list_raw_urns,
    generate_trackingId,
    generate_trackingId_as_charString,
)

def send_msg(rec,msg):
    api = Linkedin('seemyoon@gmail.com', 'karamelka2009')
    rec_public=get_id_from_urn(api.get_profile(rec)['profile_urn'])
    recs=[]
    recs.append(rec_public)
    print(recs)
    print(api.send_message(msg, recipients=recs))


# Authenticate using any Linkedin account credentials


# rec_list.append(get_id_from_urn(profile['profile_urn']))
#
# print(rec_list)
#
# print(api.send_message('Hello Kirill. Im here to suggest you to join our team',recipients=rec_list))
#
# print(api.get_profile_connections(get_id_from_urn(profile['profile_urn'])))
#
#

