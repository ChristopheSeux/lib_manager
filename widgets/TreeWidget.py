from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem,QTreeWidgetItemIterator
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QIcon
from ..functions import get_css,icon_path, get_asset_from_xml,read_json

import os

working_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
settings = read_json(os.path.join(working_dir,"settings.json"))

class TreeWidget(QTreeWidget) :
    def __init__(self,filter=None):
        super().__init__()
        self.header().close()
        self.setStyleSheet(get_css('TreeWidget'))
        self.setAlternatingRowColors(True)
        self.setIndentation(15)
        self.createWidget()


    def is_folder_in_path(self,path):
        for file in os.listdir(path) :
            full_path = os.path.join(path,file)
            if os.path.isdir(full_path) :
                return True
        return False

    def create_tree(self,path,area,step_filter) :
        #print(QTreeWidgetItemIterator(self))
        tree_root = self.invisibleRootItem() #QTreeWidgetItem(self, [os.path.basename(path).title(),path,'root'])

        for root,folders,files in os.walk(path) :
            item_path = None
            for f in files :
                item_name,item_extension = os.path.splitext(f)
                if item_extension == '.json' :
                    item_full_path = os.path.normpath(os.path.join(root,f))
                    # get the path in a list
                    item_path = item_full_path.replace(path,'').split(os.sep)[1:-1]
                    if item_path[-1]==item_name :
                        item_path = item_path[:-1]
                    break


            if item_path :
                temp_root = tree_root

                folder_path = path
                for folder in item_path :
                    folder_path = os.path.join(folder_path,folder)
                    childs = [temp_root.child(i) for i in range(temp_root.childCount())]
                    if folder not in [c.text(1) for c in childs] :
                        temp_root = QTreeWidgetItem(temp_root, [folder.title().replace('_',' '),folder])
                        temp_root.full_path = folder_path
                    else :
                        temp_root = [c for c in childs if c.text(1)==folder][0]
                        #temp_root = folder

                #read_json(item_full_path)


        '''
        asset_list={}
        for root,folders,files in os.walk(path) :
            for f in files :
                if os.path.splitext(f)[1] == '.xml' :
                    xml_path = os.path.join(root,f)
                    asset_info = get_asset_from_xml(xml_path,'Model')

                    asset = asset_info['name']
                    cat = asset_info['category']
                    folder = asset_info['folder']
                    item_type = asset_info['item_type']

                    if not asset_list.get(item_type) :
                        type_item = QTreeWidgetItem(path_item, [item_type.title(),item_type,'item_type'])
                        asset_list[item_type]={'item' :type_item,'childs':{}}

                    if not folder in asset_list[item_type]['childs'].keys() :
                        folder_item = QTreeWidgetItem(asset_list[item_type]['item'], [folder.title(),folder,'asset'])
                        asset_list[item_type]['childs'][folder] = {'item' :folder_item,'childs':{}}

                    if not cat in asset_list[item_type]['childs'][folder]['childs'].keys() :
                        category_item = QTreeWidgetItem(asset_list[item_type]['childs'][folder]['item'], [cat.title(),cat,'category'])

                        asset_list[item_type]['childs'][folder]['childs'][cat]={'item' :category_item,'childs':[]}

                    asset_list[item_type]['childs'][folder]['childs'][cat]['childs'].append(asset_info)

        self.asset_tree = asset_list
        print(asset_list)




        for fileName in os.listdir(path) :
            if fileName not in path_settings['exclude'] :
                category = os.path.join(path,fileName)
                category_item = QTreeWidgetItem(path_item, [fileName.title(),category,'category'])

                for fileName in os.listdir(category) :
                    asset = os.path.join(category,fileName)

                    if os.path.isdir(asset) :
                        asset_item = QTreeWidgetItem(category_item, [fileName.title(),asset,'asset'])

                        if area == 'Library' :

                            for fileName in os.listdir(asset) :
                                step = os.path.join(asset,fileName)


                                if fileName == step_filter and os.listdir(step):
                                    for fileName in os.listdir(step) :
                                        cat_item = QTreeWidgetItem(asset_item, [fileName.title(),step,'step'])

                                #for fileName in os.listdir(step) if filename == filter :
        '''

        self.sortItems(0, Qt.AscendingOrder)

    def recursive_dir(self,path,path_settings,item,starting_level) :

        for fileName in os.listdir(path) :
            full_path = os.path.join(path,fileName)
            level = full_path.count(os.sep)-starting_level
            if fileName not in path_settings['exclude'] and os.path.isdir(full_path) and self.is_folder_in_path(full_path)  :
                if level == 1 :
                    font = QFont("Gill Sans",9)#QFont.Bold
                    icon = QIcon(icon_path('ICON_FOLDER'))
                else :
                    font = QFont("Gill Sans",10-level)
                    icon = QIcon(icon_path('ICON_SMALL_FOLDER'))

                try :
                    int(fileName)
                except ValueError:
                    pass

                name = QTreeWidgetItem(item, [fileName.title(),full_path])
                #name.setIcon(0,icon)
                name.setFont(0,font)
                #full_path = QTreeWidgetItem(item,[full_path])
                #item =
                self.recursive_dir(full_path,path_settings,name,starting_level)

    def createWidget(self):
        #self.setStyleSheet(self.style_tree_view)
        #self.setStyleSheet("border: 10px solid #d9d9d9;")
        '''
        for path, path_settings in self.folder.items() :
            self.recursive_dir(path,path_settings,self,path.count(os.sep))
        '''
        self.create_tree(settings['path'],'Library','All')
