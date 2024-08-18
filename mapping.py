#we use atom.tag as the site_tag;
#       atom.charge as the site_adb

#here is the adb_mapping


adb_list=['*','OH','H']

def adbname_to_numindex(adbname):

    adb_list=['*','OH','H']
    numindex = adb_list.index(adbname)

    return numindex

def numindex_to_adbname(numindex):

    adb_list=['*','OH','H']
    adbname = adb_list[int(numindex)]

    return adbname
