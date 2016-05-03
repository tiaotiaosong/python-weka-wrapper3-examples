# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# build_save_clusterer.py
# Copyright (C) 2015-2016 Fracpete (pythonwekawrapper at gmail dot com)

import os
import tempfile
import traceback
import weka.core.jvm as jvm
import wekaexamples.helper as helper
from weka.clusterers import Clusterer
from weka.flow.control import Flow, ContainerValuePicker
from weka.flow.source import FileSupplier
from weka.flow.transformer import LoadDataset, Train
from weka.flow.sink import Console, ModelWriter


def main():
    """
    Just runs some example code.
    """

    # setup the flow
    helper.print_title("build and save clusterer")
    iris = helper.get_data_dir() + os.sep + "iris_no_class.arff"

    flow = Flow(name="build and save clusterer")

    filesupplier = FileSupplier()
    filesupplier.config["files"] = [iris]
    flow.actors.append(filesupplier)

    loaddataset = LoadDataset()
    flow.actors.append(loaddataset)

    train = Train()
    train.config["setup"] = Clusterer(classname="weka.clusterers.SimpleKMeans")
    flow.actors.append(train)

    pick = ContainerValuePicker()
    pick.config["value"] = "Model"
    flow.actors.append(pick)

    console = Console()
    pick.actors.append(console)

    writer = ModelWriter()
    writer.config["output"] = str(tempfile.gettempdir()) + os.sep + "simplekmeans.model"
    flow.actors.append(writer)

    # run the flow
    msg = flow.setup()
    if msg is None:
        print("\n" + flow.tree + "\n")
        msg = flow.execute()
        if msg is not None:
            print("Error executing flow:\n" + msg)
    else:
        print("Error setting up flow:\n" + msg)
    flow.wrapup()
    flow.cleanup()

if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
