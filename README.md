# ShopifyBackend
[Shopify Backend Developer Intern Challenge](https://docs.google.com/document/d/1z9LZ_kZBUbg-O2MhZVVSqTmvDko5IJWHtuFmIu_Xg1A/) for Summer 2022 by Kevin Lin

![alt text](demo.gif)
# Instructions to use:

1. Install the latest version of Python. For a good guide on installing Python, see [here](https://realpython.com/installing-python/).
You'll know you've installed Python when you can open a new terminal (Command Prompt on Windows, Terminal on Mac/Linux) and input `python --version` and have it reflect
the version that you just downloaded.
2. Clone this repository.
3. Use `cd path/to/ShopifyBackend` in a terminal to enter the directory that you just cloned (this repository). Replace `path/to/ShopifyBackend` to whatever diretory you cloned to.
4. Use the pip command in a terminal to install dependencies (pip comes with Python): `pip install -r requirements.txt`. This will install Streamlit, the UI framework.
5. Use `streamlit run main.py` in a terminal to run the web app. The terminal will tell you which localhost link you'll be able to see the website on. The default is [http://localhost:8501](http://localhost:8501). Click the link/copy it into a browser to visit it.
6. Use the form in the center of the screen to add items. Once saved, they will be in the inventory list on the left. You can click on any of the created items
to edit or delete them. This satisfies the CRUD functionality.
7. Use the Download CSV button to export the data to CSV.

# Future feature development considerations
Streamlit (and Python) is made for prototyping, and so it is a little slow in comparison to other languages. Nonetheless,
their strengths are evident in the easy UI that took a couple of hours to make. 

For new fields to be added to the camera's details, they simply have to be added as widgets in the forms. This could be abstracted away
to be even easier by storing the inventory variable widget type in a config json/yaml file. 

Because this is Python, the things (namely API calls) that could plug and play into this UI is endless. Streamlit websites
are also pretty easy to host in Dockerized containers.
