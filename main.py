import os, sys, xml.etree.ElementTree, shutil
def find_folders():
    for item in os.listdir():
        if os.path.isfile(item):
            continue
        else:   
            yield item
main = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
try:
    os.mkdir(main+'/Making de pack')
    os.mkdir(main+'/You can delete it')
except:
    pass

os.chdir("LocalMods")
for folder in find_folders():
    try:
        root = xml.etree.ElementTree.parse(main+'/LocalMods/'+folder+'/filelist.xml').getroot()
        #print(folder+': '+root.attrib['name'])
        f = open(main+'/You can delete it/'+root.attrib['name']+'.txt', 'w')
        f.write(folder)
        f.close()
    except:
        pass

e = xml.etree.ElementTree.parse(main+'/ModLists/mods.xml').getroot()

for child in e.iter('Local'):
    f = open(main+'/You can delete it/'+child.attrib['name']+'.txt', 'r')
    get_id = f.read()
    f.close()
    #print(get_id)
    source_dir = main+'/LocalMods/'+get_id+'/'
    #print(source_folder)
    destination_dir = main+'/Making de pack/'+get_id+'/'
    shutil.copytree(source_dir, destination_dir)

shutil.make_archive(main+'/Making de pack.zip', 'zip', main+'/Making de pack')