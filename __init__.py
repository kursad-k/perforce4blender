import os
import sys
from pathlib import Path
import time
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
from P4 import P4

import bpy

bl_info = {
    "name": "Perforce4Blender",
    "author": "Kursad Karatas",
    "version": (0, 1),
    "blender": (2, 92, 0),
    "location": "File > Import-Export",
    "description": "Export scene",
    "warning": "",
    "category": "Import-Export",
}

def MessageBox(message="", title="Message Box", icon='INFO', lines=""):

    def draw(self, context):
        for n in lines:
            self.layout.label(text=n)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def getFileName():
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = os.path.splitext(filename)[0]

    return filename


def getFilePath():
    return bpy.context.blend_data.filepath


def p4Setup():

    p4 = P4()

    p4.connect()
    info = p4.run("info")
    print(info)


def p4():

    p4 = P4()
    return p4


def p4Add(file):

    p4 = P4()

    with p4.connect():
        p4.connect()
        print(p4.run("info"))

        p4.run("add", file)

    return


def p4Checkout(file):

    p4 = P4()

    with p4.connect():
        print(p4.run("info"))

        p4.run_edit(file)
        print("Checked out {}".format(file))

    return


def p4Submit(file, commitlog=""):

    p4 = P4()

    p4.connect()
    print(p4.run("info"))

    change = p4.fetch_change()
    change._description = commitlog

    print(change)

    p4.run_submit(change)


def p4ListChangeList(self):

    p4 = P4()
    p4.password = "temp"

    with p4.connect():
        print(p4.run("info"))

        change = p4.fetch_change()
        print(change)

        msg = ""

        if "Files" in change.keys():

            msg = change["Files"]

        else:
            msg = ["No files in the changelist"]

        MessageBox(message=msg, title="Current Changelist", lines=msg)


class P4BLENDER_OT_P4Add(bpy.types.Operator):
    """ """
    bl_label = "Add the current scene to perforce"
    bl_idname = "scene._p4add"
    bl_category = "Perforce"

    def execute(self, context):
        scene = context.scene

        curr_file = Path(getFilePath())
        p4Add(curr_file)

        return {'FINISHED'}


class P4BLENDER_OT_P4Checkout(bpy.types.Operator):
    """ """
    bl_label = "Checkout the current scene to perforce"
    bl_idname = "scene._p4checkout"
    bl_category = "Perforce"

    def execute(self, context):

        scene = context.scene

        curr_file = getFilePath()

        p4Checkout(curr_file)

        return {'FINISHED'}


class P4BLENDER_OT_P4Submit(bpy.types.Operator):
    """ """
    bl_label = "Submit the current scene to perforce"
    bl_idname = "scene._p4submit"
    bl_category = "Perforce"

    commitlog: bpy.props.StringProperty(name="CommitLog")

    def execute(self, context):
        scene = context.scene

        curr_file = getFilePath()

        p4Submit(curr_file, self.commitlog)

        print(self.commitlog)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class P4BLENDER_OT_P4Changelist(bpy.types.Operator):
    """ """
    bl_label = "List changelist"
    bl_idname = "scene._p4changelist"
    bl_category = "Perforce"

    commitlog: bpy.props.StringProperty(name="CommitLog")

    def execute(self, context):
        scene = context.scene

        p4ListChangeList(self)

        return {'FINISHED'}


class P4BLENDER_OT_P4Sync(bpy.types.Operator):
    """ """
    bl_label = "Syncs the workpspace"
    bl_idname = "scene._p4sync"
    bl_category = "Perforce"

    commitlog: bpy.props.StringProperty(name="CommitLog")

    def execute(self, context):
        scene = context.scene

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class P4BLENDER_OT_P4Revert(bpy.types.Operator):
    """ """
    bl_label = "Removes it from the change list"
    bl_idname = "scene._p4revert"
    bl_category = "Perforce"

    commitlog: bpy.props.StringProperty(name="CommitLog")

    def execute(self, context):
        scene = context.scene

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class P4BLENDER_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "P4BLENDER_PT_exporterpanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Perforce"
    bl_category = "Z"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene

        layout = self.layout

        row = layout.row()
        row.label(text="Perforce", icon='WORLD_DATA')

        row = layout.row()
        row.operator("scene._p4add", text="Add")

        row = layout.row()
        row.operator("scene._p4checkout", text="Checkout")

        row = layout.row()
        row.operator("scene._p4submit", text="Submit")

        row = layout.row()
        row.operator("scene._p4sync", text="Sync")

        row = layout.row()
        row.operator("scene._p4changelist", text="Changelist")


classes = (
    P4BLENDER_OT_P4Add,
    P4BLENDER_OT_P4Submit,
    P4BLENDER_OT_P4Checkout,
    P4BLENDER_OT_P4Sync,
    P4BLENDER_OT_P4Changelist,
    P4BLENDER_PT_Panel,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
