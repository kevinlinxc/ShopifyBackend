import streamlit as st
import json
import datetime
from dataclasses import dataclass


def page_setup():
    st.set_page_config(page_title="Shopify Camera Inventory Tracker", page_icon="camera.png")
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@dataclass
class CameraItem:
    name: str
    brand: str
    received_day: str
    notes: str


class CameraInventory:

    def __init__(self):
        page_setup()
        if "items" in st.session_state:
            self.items = json.loads(st.session_state["items"])
        else:
            self.items = {}
        self.sidebar = st.sidebar
        self.create_inventory()

    def update_focus(self, focus, name=None, brand=None, received_day=None, notes=None, canonical_name=None):
        st.session_state["focus"] = focus
        if name:
            dict_to_save = CameraItem(name, brand, received_day.strftime("%d/%m/%Y"), notes).__dict__
            self.items[canonical_name] = dict_to_save
            items_to_json = json.dumps(self.items)
            st.session_state["items"] = items_to_json

    def delete_item(self, item):
        st.session_state["focus"] = "none"
        self.items.pop(item)
        items_to_json = json.dumps(self.items)
        st.session_state["items"] = items_to_json

    def create_inventory(self):
        # create sidebar to add items or edit existing items

        camera_brands = ["Canon", "Nikon", "Sony", "Panasonic", "Pentax"]
        # make default functionality of center of web app adding a new item
        st.session_state["focus"] = st.session_state.get("focus", "new")
        if self.sidebar.button("Add a new item", help="Click to add a new item"):
            # use session state to change center of page's function instead of variables, since Streamlit runs
            # top to bottom every time a widget is interacted with so variables would not work
            st.session_state["focus"] = "new"
        # visual separator
        self.sidebar.markdown("---------")

        if st.session_state["focus"] == "new":
            # user is on the new item creation screen
            with st.form(key='new_form'):
                # display new item dialogue
                st.markdown("# Add a new item")
                name = st.text_input("Camera name:", help="User friendly name for camera",
                                     value=f"Camera {len(self.items.items()) + 1}")
                now = datetime.datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                canonical_name = name + dt_string
                brand = st.selectbox("Camera brand:", options=camera_brands, help="brand of the camera")
                received_day = st.date_input("Date when camera entered inventory:",
                                             help="Year that the camera model was released")
                notes = st.text_area("Notes", value="e.g. quality of camera")
                st.form_submit_button("Save", on_click=self.update_focus, args=["none", name, brand, received_day, notes, canonical_name])
            self.refresh_sidebar()

        elif st.session_state["focus"] == "none":
            # user has just saved a new item/edited another item
            st.markdown("Click an item to see its information, or add a new item")
            self.refresh_sidebar()

        else:
            # user has clicked on an inventory item, and wants to edit it
            # a bit DRY, but the abstracted function would honestly be more confusing to read

            canonical_name = st.session_state["focus"]
            item_to_edit = self.items[canonical_name]
            st.markdown(f"# Editing/Viewing {item_to_edit['name']}")
            name = st.text_input("Camera name:", help="User friendly name for camera",
                                 value=f"{item_to_edit['name']}")
            brand = st.selectbox("Camera brand:", options=camera_brands, help="brand of the camera", index=camera_brands.index(item_to_edit['brand']))
            reformatted_date = datetime.datetime.strptime(item_to_edit['received_day'], "%d/%m/%Y")
            received_day = st.date_input("Date when camera entered inventory:",
                                         help="Year that the camera model was released", value=reformatted_date)
            notes = st.text_area("Notes", value=item_to_edit['notes'])
            st.button("Save edits", on_click=self.update_focus,
                                  args=["none", name, brand, received_day, notes, canonical_name])
            st.button("Delete", on_click=self.delete_item, args=[canonical_name])
            self.refresh_sidebar()

    def refresh_sidebar(self):
        if len(self.items.items()) > 0:
            self.sidebar.markdown("# Current Inventory:")
        for name in self.items:
            camera_item = self.items[name]
            self.sidebar.button(camera_item["name"] + " Created on: " + camera_item["received_day"],
                                help="Click to edit", key=name, on_click=self.update_focus, args=[name])


def main():
    CameraInventory()


# good practice in python to avoid import errors
if __name__ == "__main__":
    main()
