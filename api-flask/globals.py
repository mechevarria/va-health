import ayasdi.core as ac

user = {}

def get_all_group_id(src):
    '''Returns the ID for the default group / no filters applied'''

    grp = src.create_group(name='all_rows')
    applied_filter = {"id": grp['id'], "name": "all_rows"}
    return applied_filter