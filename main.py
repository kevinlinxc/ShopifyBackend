"""Main code for Shopify Backend Coding Challenge. Made by Kevin Lin."""
import streamlit as st
import json
import datetime
from dataclasses import dataclass
import csv
from enum import Enum


def page_setup():
    """Streamlit page setup function."""
    st.set_page_config(
        page_title="Shopify Camera Inventory Tracker", page_icon="camera.png"
    )
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


class Focus(Enum):
    """Enum used to abstract hardcoded strings."""

    new = "new"
    none = "none"


@dataclass
class CameraItem:
    """
    Simple information storage for Camera Item.

    Could be replaced with a dict, but this could have better
    functionality in the future with __repr__ and __hash__ and custom functions.
    """

    name: str
    brand: str
    received_day: str
    notes: str


class CameraInventory:
    """Main class of this web app."""

    def __init__(self):
        """
        Initialize Camera Inventory.

        Loads session state items so page can be reloaded with persisting items.
        Entry point for web app.
        """
        page_setup()
        if "items" in st.session_state:
            self.items = json.loads(st.session_state["items"])
        else:
            self.items = {}
        self.sidebar = st.sidebar
        st.write("# Shopify Backend Camera Inventory System by Kevin Lin")
        self.create_all()

    def update_focus(
        self,
        focus,
        name=None,
        brand=None,
        received_day=None,
        notes=None,
        backend_name=None,
    ):
        """
        General use callback to update main section of website or add item to inventory (normally done together).

        :param focus: What to change the focus to.
        :param name: Name of camera entered by user
        :param brand: Brand of camera
        :param received_day: Day hypothetical camera was received into inventory
        :param notes: Notes about camera from user
        :param backend_name: Unique name used in this program in the backend
        :return: None
        """
        st.session_state["focus"] = focus
        if name:
            dict_to_save = CameraItem(
                name, brand, received_day.strftime("%d/%m/%Y"), notes
            ).__dict__
            self.items[backend_name] = dict_to_save
            items_to_json = json.dumps(self.items)
            st.session_state["items"] = items_to_json

    def delete_item(self, item):
        """
        Delete an item from inventory.

        Is a callback function.

        :param item: backend name of item to delete
        :return: None. Modifies session_state
        """
        st.session_state["focus"] = Focus.none
        self.items.pop(item)
        items_to_json = json.dumps(self.items)
        st.session_state["items"] = items_to_json

    def create_all(self):
        """
        Create the main portions of the website.

        Changes what the middle of the screen shows, depending on if the user wants to add a new item, wants to edit
        an existing one, or has nothign selected.

        :return: None
        """
        # create sidebar to add items or edit existing items

        camera_brands = ["Canon", "Nikon", "Sony", "Panasonic", "Pentax"]
        # make default functionality of center of web app adding a new item
        st.session_state["focus"] = st.session_state.get("focus", Focus.new)
        if self.sidebar.button("Add a new item", help="Click to add a new item"):
            # use session state to change center of page's function instead of variables, since Streamlit runs
            # top to bottom every time a widget is interacted with so variables would not work
            st.session_state["focus"] = Focus.new
        # visual separator
        self.sidebar.markdown("---------")

        if st.session_state["focus"] == Focus.new:
            # user is on the new item creation screen
            # display new item dialogue
            st.markdown("# Add a new item")
            name = st.text_input(
                "Camera name:",
                help="User friendly name for camera",
                value=f"Camera {len(self.items.items()) + 1}",
            )
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            backend_name = name + dt_string
            brand = st.selectbox(
                "Camera brand:", options=camera_brands, help="brand of the camera"
            )
            received_day = st.date_input(
                "Date when camera entered inventory:",
                help="Year that the camera model was released",
            )
            notes = st.text_area("Notes", value="e.g. quality of camera")
            st.button(
                "Save",
                on_click=self.update_focus,
                args=[Focus.none, name, brand, received_day, notes, backend_name],
            )
            self.refresh_inventory()

        elif st.session_state["focus"] == Focus.none:
            # user has just saved a new item/edited another item
            st.markdown("Click an item to see/edit its information, or add a new item")
            self.refresh_inventory()

        else:
            # user has clicked on an inventory item, and wants to edit it
            # a bit DRY, but the abstracted function would honestly be more confusing to read
            backend_name = st.session_state["focus"]
            item_to_edit = self.items[backend_name]
            st.markdown(f"# Editing/Viewing {item_to_edit['name']}")
            name = st.text_input(
                "Camera name:",
                help="User friendly name for camera",
                value=f"{item_to_edit['name']}",
            )
            brand = st.selectbox(
                "Camera brand:",
                options=camera_brands,
                help="brand of the camera",
                index=camera_brands.index(item_to_edit["brand"]),
            )
            reformatted_date = datetime.datetime.strptime(
                item_to_edit["received_day"], "%d/%m/%Y"
            )
            received_day = st.date_input(
                "Date when camera entered inventory:",
                help="Year that the camera model was released",
                value=reformatted_date,
            )
            notes = st.text_area("Notes", value=item_to_edit["notes"])
            st.button(
                "Save edits",
                on_click=self.update_focus,
                args=[Focus.none, name, brand, received_day, notes, backend_name],
            )
            st.button("Delete", on_click=self.delete_item, args=[backend_name])
            self.refresh_inventory()

    def refresh_inventory(self):
        """
        Refresh the inventory in the sidebar after a button callback has modified the inventory.

        :return: None
        """
        if len(self.items.items()) > 0:
            self.sidebar.markdown("# Current Inventory:")
            with open("file.csv", "w", newline="") as csvfile:
                fieldnames = ["backend_name", "name", "brand", "received_day", "notes"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for backend_name in self.items:
                    item_dict_copy = self.items[backend_name].copy()
                    item_dict_copy["backend_name"] = backend_name
                    writer.writerow(item_dict_copy)
            with open("file.csv", "r") as f:
                self.sidebar.download_button(
                    "Download CSV",
                    f,
                    mime="text/csv",
                    file_name="shopify_backend_kevinlinxc.csv",
                )

        for name in self.items:
            camera_item = self.items[name]
            self.sidebar.button(
                camera_item["name"] + " Created on: " + camera_item["received_day"],
                help="Click to edit",
                key=name,
                on_click=self.update_focus,
                args=[name],
            )


def main():
    """Simply spawns a Camera Inventory object. Every time the site is refreshed."""
    CameraInventory()


# good practice in python to avoid import errors
if __name__ == "__main__":
    main()
