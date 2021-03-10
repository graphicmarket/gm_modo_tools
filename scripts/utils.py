# python
# coding=utf8

#python
import modo
import lx
from re import search
from slugify import slugify

arg = lx.arg()
scene = modo.Scene()

SHADING = ['mask', 'polyRender', 'occlusion', 'defaultShader', 'advancedMaterial', 'renderOutput', 'videoBlank', 'imageMap', '*Light', 'light*', 'environment', 'scene']
ITEMS = ['mesh', 'groupLocator', 'camera', 'locator', '*Light', 'portal', 'falloff.*', '*.falloff', 'curveParam']
GROUPS = [1, 'render', 'actionclip']

selected = scene.selected

def renameObject(obj, new_name):
    obj.select(True)
    lx.eval('item.name "{0}"'.format(new_name)) # Have to rename with lx.eval otherwise undo doesn't work

def isInGroup(itemType, target):

    for t in target:
        if (t == itemType) or (isinstance(itemType, str) and isinstance(t, str) and (t.find('*') != -1) and (itemType.find(t.replace('*', '')) != -1)):
            return True

    return False
        

target = None

if arg == 'shading':
    target = SHADING
if arg == 'items':
    target = ITEMS
if arg == 'groups':
    target = GROUPS
# if arg == 'all':
#     target = GROUPS + SHADING + ITEMS

for item in selected:
    itemType = item.type or item.Type()
    if isInGroup(itemType, target):
	    renameObject(item, slugify(item.baseName or item.name))