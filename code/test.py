from tools.uri import uri_to_label
from tools.extend import get_text
from tools import download_sounds
from tools import fetch

uri = '/c/en/pet'
#uri = '/a/[/r/CapableOf/,/c/en/dog/,/c/en/bark/]'
#uri = '/a/[/r/HasA/,/c/en/dog/,/c/en/four_legs/]'
uri = '/c/en/dog'

#uri = '/a/[/r/CreatedBy/,/c/en/cake/,/c/en/bake/]'

#save_path = "download/person's_room"
#print(get_text(uri))
#download_sounds.download_sound(get_text(uri), save_path)
fetch.delete_uri(uri)
