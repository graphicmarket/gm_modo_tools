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

selection = scene.selected

def renameObject(obj, new_name):
    obj.select(True)
    lx.eval('item.name "{0}"'.format(new_name)) # Have to rename with lx.eval otherwise undo doesn't work

def isInGroup(itemType, target):
    for t in target:
        if (t == itemType) or (isinstance(itemType, str) and isinstance(t, str) and (t.find('*') != -1) and (itemType.find(t.replace('*', '')) != -1)):
            return True

    return False

def renameByTargetType(target):
    for item in selection:
        itemType = item.type or item.Type()
        if isInGroup(itemType, target):
            renameObject(item, slugify(item.baseName or item.name))

def restoreSelection():
    for item in selection:
        item.select()

if arg == 'shading':
    renameByTargetType(SHADING)
if arg == 'items':
    renameByTargetType(ITEMS)
if arg == 'groups':
    renameByTargetType(GROUPS)
if arg == 'last':
    item = selection[-1]
    renameObject(item, slugify(item.baseName or item.name))
# if arg == 'all':
#     renameByTargetType(GROUPS + SHADING + ITEMS)

restoreSelection()