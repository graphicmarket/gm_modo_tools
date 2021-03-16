# python

import modo
import lx
from slugify import slugify

# lx.trace( True )
scene = modo.Scene()
selectedTargetMask = []
exportableMeshes = []
globalSelection = scene.selected

def getSelectedItemsByType(type):
    """ 
        Filter Selection by type 
    """
    return filter(lambda item: item.type == type, globalSelection or [])


def getSelectedMaskItems():
    """ Get Mask Items from selection """
    return getSelectedItemsByType('mask')


def getSelectedMeshItems():
    """ Get Mesh Items from selection """
    return getSelectedItemsByType('mesh')


def getTargetGroupMask():
    """ Get the mask where the Alpha outputs will be placed """
    selection = getSelectedMaskItems()

    if len(selection) is not 0:
        return selection[0]
    else:
        showErrorDialog('Select a shading group mask first')


def showErrorDialog(msg):
    """ Show a simple error dialog """
    lx.eval('dialog.setup error')
    lx.eval('dialog.title Error')
    lx.eval('dialog.msg "%s"' % msg)
    lx.eval('dialog.open')


def selectItemById(itemId):
    """ Put the selection in a specific item by id """
    lx.eval('select.subItem ' + itemId +
            ' set textureLayer;render;environment;light;camera;scene;replicator;bake;mediaClip;txtrLocator')

def restoreSelection():
    for item in globalSelection:
        item.select()

def selectionSetsToAlphasGroupedByMeshName():
    """
        Deselect the meshes in order to avoid select one by one in the next loop
        because the the available Selection sets depending of the selected meshes
    """
    for mesh in exportableMeshes:
        mesh.deselect()

    for mesh in exportableMeshes:

        mesh.select()

        # Create Group with mesh name
        lx.eval('shader.create mask')
        lx.eval('item.name \"' + mesh.baseName + '\"')
        lx.eval('mask.setMesh \"' + mesh.name + '\"')

        # Since the las created item is add ever to selection, the last item of the selection array
        # could be the last create group so we send the id of this.
        selectionSetsToAlphas(scene.selected[-1].id, mesh.baseName)
        mesh.deselect()

        # Back selection to the target group
        selectItemById(selectedTargetMask.id)


def selectionSetsToAlphas(targetMask='', customGroupName=''):
    # number of Poly Selection Sets
    num_polset = lx.eval('query layerservice polset.N ? all')

    for i in range(num_polset):
        polset_name = lx.eval('query layerservice polset.name ? %s' % i)

        isCustomGroup = customGroupName != ''

        # Add group for Selection Set
        customGroupName = customGroupName if customGroupName != '' else '(all)'
        lx.eval('shader.create mask')
        lx.eval('mask.setMesh "%s"' % customGroupName)
        lx.eval('mask.setPTagType "Selection Set"')
        lx.eval('mask.setPTag \"' + polset_name + '\"')

        # If a created group is mixed(based in a group in the mesh) then this the way to set the name of this
        if isCustomGroup:
            lx.eval('texture.name \"' + polset_name + '\"')

        # Add render output
        lx.eval('shader.create renderOutput')
        lx.eval('shader.setEffect shade.alpha')

        if isCustomGroup:
            alphaName = slugify('Alpha ' + customGroupName + ' ' + polset_name)
        else:
            alphaName = slugify('Alpha ' + polset_name)

        lx.eval('item.name \"%s\" renderOutput' % alphaName)
        lx.eval('item.channel renderOutput$colorspace "nuke-default:sRGB"')

        # Reset selection to parent
        targetMask = targetMask if targetMask != '' else selectedTargetMask.id
        lx.out(targetMask)
        selectItemById(targetMask)


def createGroupForSelection():

    # Create a group for meshes
    lx.eval('group.create "Group" std empty')

    # Select the meshes because when a is create the selection of these is lost
    for mesh in exportableMeshes:
        mesh.select()

    # Get the created group from selection must be the only one with the type "1", that is group.
    createdGroup = filter(lambda item: item.Type() == 1, scene.selected)

    # Add the selected items to the group
    lx.eval('group.edit add item')

    # return group name
    return createdGroup[0].name


# Script argument
mode = lx.arg()
selectedTargetMask = getTargetGroupMask()
exportableMeshes = getSelectedMeshItems()

if len(exportableMeshes) == 0:
    showErrorDialog("Please, first select the target meshes")

if mode == 'ungrouped':
    selectionSetsToAlphas()
elif mode == 'grouped':
    selectionSetsToAlphasGroupedByMeshName()
elif mode == 'forGroup':
    group = createGroupForSelection()

    # Reset selection to the target mask
    selectItemById(selectedTargetMask.id)

    selectionSetsToAlphas('', group)

restoreSelection()