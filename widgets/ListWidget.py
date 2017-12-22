from PyQt5.QtWidgets import QListWidget,QListView,QAbstractItemView,QMenu,QAction,QListWidgetItem
from PyQt5.QtCore import QSize,QPoint,Qt,QDir
from PyQt5.QtGui import QIcon

from ..functions import get_css,icon_path,read_json,clear_layout
from . AssetInfo import AssetInfo

import bpy,os

working_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
settings = read_json(os.path.join(working_dir,"settings.json"))

#from .. import settings

class ListWidget(QListWidget):
    def __init__(self,parent):
        super().__init__(parent)

        #self.folder = settings.paths
        self.parent = parent
        #self.setStyleSheet(get_css('ThumbnailList'))
        #self.setViewMode(QListView.IconMode)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setStyleSheet(get_css('ThumbnailList'))
        self.setAlternatingRowColors(True)
        self.setWrapping(True)
        self.setIconSize(QSize(128, 128))
        self.setMovement(QListView.Static)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.setSortingEnabled(True)

        self.itemDoubleClicked.connect(self.menu_item_link)
        self.itemClicked.connect(self.click_thumb)

    def set_item(self,item_info,index) :
        item =QListWidgetItem(item_info['asset'])
        item.setIcon(QIcon(item_info['image']))
        item.info = item_info
        self.addItem(item)

    def on_context_menu(self, QPos):
        self.listMenu= QMenu()
        link = QAction(QIcon(icon_path('ICON_LINK_BLEND')), 'Link', self)
        link.triggered.connect(self.menu_item_link)

        append = QAction(QIcon(icon_path('ICON_APPEND_BLEND')), 'Append', self)
        append.triggered.connect(self.menu_item_append)

        delete = QAction(QIcon(icon_path('ICON_CLOSE')), 'Delete', self)
        delete.triggered.connect(self.menu_item_delete)

        self.listMenu.addAction(link)
        self.listMenu.addAction(append)
        self.listMenu.addAction(delete)
        #menu_item.connect(self.menuItemClicked)
        parentPosition = self.mapToGlobal(QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()


    # display information when clicking on a thumbnail
    def click_thumb(self,item) :
        clear_layout(self.parent.rightLayout)

        item_info = item.info

        self.AssetInfo = AssetInfo(self.parent,item_info)

        self.parent.rightLayout.addLayout(self.AssetInfo)


    def menu_item_link(self) :
        #from .. import asset_loading
        asset_list = self.parent.asset_list
        asset_type = self.parent.asset_type
        selected_rows = [i.row() for i in self.selectionModel().selectedRows()]
        self.offset = 0
        print('####')
        #print([i['info'] for i in self.selectedItems()])
        #self.scene = bpy.context.scene
        for item in self.selectedItems() :
            from .. import asset_managing as asset_managing
            load_func = asset_type[item.info['type']]['load']

            module = getattr(asset_managing,item.info['type'])
            getattr(module,load_func)(self.parent,self,item.info,link=True)

            self.offset +=1

    def menu_item_append(self) :
        #from .. import asset_loading
        asset_list = self.parent.asset_list
        asset_type = self.parent.asset_type
        selected_rows = [i.row() for i in self.selectionModel().selectedRows()]
        self.offset = 0
        #self.scene = bpy.context.scene
        for index in selected_rows:
            from .. import asset_managing as asset_managing
            load_func = asset_type[asset_list[index]['type']]['load']

            module = getattr(asset_managing,asset_list[index]['type'])
            getattr(module,load_func)(self.parent,self,asset_list[index],link=False)

            self.offset +=1

    def menu_item_delete(self) :
        #self.parent.treeWidget.clear()
        asset_list = self.parent.asset_list
        selected_rows = [i.row() for i in self.selectionModel().selectedRows()]
        import shutil
        paths = [asset_list[i].info['info_path'] for i in selected_rows]
        #self.parent.thumbnailList.clear()
        #self.parent.treeWidget.setCurrentItem(self.parent.treeWidget.headerItem())
        for path in paths:
            #self.takeItem(self.row(item))
            shutil.rmtree(os.path.dirname(path),ignore_errors=True)
