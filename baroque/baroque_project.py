import os
import sys


class BaroqueProject(object):
    """ Stores details about the current project.

    It takes a source_directory and a destination_directory.
    source_directory: Either a shipment, collection, or item directory
    destination_directory: Location to store reports generated by baroque

    An initial instantiation of this object might look like:

    {
        "items": [
            {
            "id": "",
            "path": "",
            "files": {
                "wav": [],
                "mp3": [],
                "jpg": [],
                "xml": [],
                "md5": [],
                "txt": []
            },
            "errors": []
            }
        ],
        "source": source_directory,
        "destination": destination_directory
    }
    """

    def __init__(self, source_directory, destination_directory):
        if not os.path.exists(source_directory):
            print("source_directory does not exist")
            sys.exit()
        if not os.path.exists(destination_directory):
            print("destination_directory does not exist")
            sys.exit()

        self.source_directory = source_directory
        self.destination_directory = destination_directory

        self.shipment = []
        self.collections = []
        self.items = []

        self.source_type = self.characterize_source_directory()
        if self.source_type == "shipment":
            self.process_shipment(source_directory)
        elif self.source_type == "collection":
            self.process_collection(source_directory)
        elif self.source_type == "item":
            self.process_item(source_directory)

    def characterize_source_directory(self):
        character_directory_name = os.path.basename(self.source_directory)
        character_directory_dirs = []
        character_directory_files = []

        for dir_entry in os.scandir(self.source_directory):
            if dir_entry.is_file():
                character_directory_files.append(str(dir_entry.name))
            elif dir_entry.is_dir():
                character_directory_dirs.append(str(dir_entry.name))

        print(character_directory_dirs)
        print(character_directory_files)

        if len(character_directory_files) > 0 and len(character_directory_dirs) == 0:
            if all([filename.startswith(character_directory_name) for filename in character_directory_files]):
                return "item"
            else:
                print("source_directory looks like an item but has unexpected filenames")
                sys.exit()
        elif len(character_directory_dirs) > 0:
            if any([directory.startswith(character_directory_name) for directory in character_directory_dirs]):
                return "collection"
            else:
                return "shipment"
        else:
            print("source_directory is empty")
            sys.exit()

    def process_shipment(self, shipment_directory):
        self.shipment.append({
            "id": os.path.basename(shipment_directory),
            "path": shipment_directory
        })

        for dir_entry in os.scandir(shipment_directory):
            if dir_entry.is_dir():
                self.process_collection(dir_entry.path)

    def process_collection(self, collection_directory):
        self.collections.append({
            "id": os.path.basename(collection_directory),
            "path": collection_directory
        })

        for dir_entry in os.scandir(collection_directory):
            if dir_entry.is_dir():
                self.process_item(dir_entry.path)

    def process_item(self, item_directory):
        files = {"wav": [], "mp3": [], "jpg": [], "xml": [], "md5": [], "txt": [], "other": []}

        file_formats = {
            "wav": ["wav", "wave"],
            "mp3": ["mp3"],
            "jpg": ["jpg", "jpeg", "jpe", "jif", "jfif", "jfi"],
            "xml": ["xml"],
            "md5": ["md5"],
            "txt": ["txt"]
        }

        for file in os.listdir(item_directory):
            other = True
            extension = file.lower().split(".")[-1]

            for format, extensions in file_formats.items():
                if extension in extensions:
                    files[format].append(file)
                    other = False

            if other is True:
                files["other"].append(file)

        self.items.append({
            "id": os.path.basename(item_directory),
            "path": item_directory,
            "files": files
        })
