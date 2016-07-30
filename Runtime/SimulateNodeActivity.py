__author__ = "Subhav Pradhan"

import getopt
import sys
from pymongo import MongoClient
from InvokeManagementEngine import invoke_management_engine

def execute_action():
    client = MongoClient("localhost")
    db = client["ConfigSpace"]
    nColl = db["Nodes"]


    if START_ACTION:
        print "STARTING node:", NODE_NAME

        # Create object to store in database.
        nodeToAdd = dict()
        nodeToAdd["name"] = NODE_NAME
        nodeToAdd["nodeTemplate"] = NODE_TEMPLATE
        nodeToAdd["status"] = "ACTIVE"

        interfaceToAdd = dict()
        interfaceToAdd["name"] = ""
        interfaceToAdd["address"] = "127.0.0.1:"+NODE_PORT
        interfaceToAdd["network"] = ""

        nodeToAdd["interfaces"] = list()
        nodeToAdd["interfaces"].append(interfaceToAdd)

        nodeToAdd["processes"] = list()

        # NOTE: Update used with upsert instead of insert because
        # we might be adding node that had previously failed or
        # been removed.
        nColl.update({"name":NODE_NAME}, nodeToAdd, upsert = True)

        # Check if any application already exists. If there are
        # applications then it means that the node join has to
        # be treated as hardware update and therefore the solver
        # should be invoked. If there are no applications then
        # this node is addition is happening at system initialization
        # time so do not invoke the solver.
        systemInitialization = True

        if "GoalDescriptions" in db.collection_names():
            gdColl = db["GoalDescriptions"]
            if gdColl.count() != 0:
                systemInitialization = False

        if not systemInitialization:
            # Using localhost as management engine address since that will always
            # be the case for simulation.
            invoke_management_engine("localhost", "localhost", True)
    elif STOP_ACTION:
        print "STOPPING node:", NODE_NAME

        # Mark node faulty.
        nColl.update({"name":NODE_NAME, "status":"ACTIVE"},
                     {"$set": {"status":"FAULTY"}})

        # Store names of affected component instances.
        findResults = nColl.find({"name":NODE_NAME, "status":"FAULTY"})
        failedComponentInstances = list()

        from SolverBackend import Serialize

        for findResult in findResults:
            node = Serialize(**findResult)
            for p in node.processes:
                process = Serialize(**p)
                for c in process.components:
                    component = Serialize(**c)
                    failedComponentInstances.append(component.name)

        # Update ComponentInstances collection using above collected information.
        ciColl = db["ComponentInstances"]
        for compInst in failedComponentInstances:
            ciColl.update({"name":compInst},
                          {"$set":{"status":"FAULTY"}})

        # Pull all processes.
        nColl.update({"name":NODE_NAME, "status":"FAULTY"},
                     {"$pull":{"processes":{"name":{"$ne":"null"}}}})

        # Using localhost as management engine address since that will always
        # be the case for simulation.
        invoke_management_engine("localhost", "localhost", False)

def print_usage():
    print "USAGE:"
    print "SimulateNodeActivity --nodeName <node name> --nodeTemplate <node template name> " \
          "--port <unique port number for DM> --action <'start' | 'stop'>"

def main():
    global NODE_NAME
    global NODE_TEMPLATE
    global NODE_PORT
    global START_ACTION
    global STOP_ACTION

    NODE_NAME = None
    NODE_TEMPLATE = None
    NODE_PORT = None
    START_ACTION = False
    STOP_ACTION = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hntpa",
                                   ["help", "nodeName=", "nodeTemplate=","port=", "action="])
    except getopt.GetoptError:
        print 'Cannot retrieve passed parameters.'
        print_usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-n", "--nodeName"):
            print "Node name:", arg
            NODE_NAME = arg
        elif opt in ("-t", "--nodeTemplate"):
            print "Node template name:", arg
            NODE_TEMPLATE = arg
        elif opt in ("-p", "--port"):
            print "Port number:", arg
            NODE_PORT = arg
        elif opt in ("-s", "--action"):
            print "Action:", arg
            if arg == "start":
                START_ACTION = True
            elif arg == "stop":
                STOP_ACTION = True
            else:
                print_usage()
                sys.exit()

    if (NODE_NAME is None):
        print "Node name not provided!"
        print_usage()
        sys.exit()

    if (START_ACTION and (NODE_TEMPLATE is None or NODE_PORT is None)):
        print "Node template and/or node port not provided!"
        print_usage()
        sys.exit()

    # Add action affects to the database.
    execute_action()

if __name__ == '__main__':
    main()
