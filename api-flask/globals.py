import ayasdi.core as ac

user = {}

def get_all_group_id():
    '''Returns the ID for the default group / no filters applied'''

    src = user['connection'].get_source(name=user['source_name'])
    grp = src.create_group(name='all_rows')
    applied_filter = {"id": grp['id'], "name": "all_rows"}
    return applied_filter