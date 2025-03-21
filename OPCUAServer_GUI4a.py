#
# If moved edit standard library at:
# C:\Users\Administrator\AppData\Local\Programs\Python\Python310\Lib\site-packages\asyncua\crypto\validator.py:81
# from datetime import datetime, timezone
# now = datetime.now(timezone.utc)
#
# C:\Users\Administrator\AppData\Local\Programs\Python\Python310\Lib\site-packages\asyncua\server\internalserver.py:107 URI change
# C:\Users\Administrator\AppData\Local\Programs\Python\Python310\Lib\site-packages\asyncua\server\server.py:89
#

from typing import List
from cryptography import x509
from datetime import datetime, timedelta
# , load_pem_private_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509.oid import ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from asyncua.crypto.uacrypto import load_certificate,  load_private_key
from asyncua.crypto.cert_gen import generate_private_key, generate_self_signed_app_certificate, dump_private_key_as_pem, generate_app_certificate_signing_request, sign_certificate_request
from os import listdir  # , path, getcwd
from asyncua.crypto.validator import CertificateValidator, CertificateValidatorOptions
from asyncua.server.user_managers import CertificateUserManager
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua import ua
from asyncua import Server
from random import uniform
import logging
import asyncio
from pathlib import Path
# from csv import reader
import socket
import FreeSimpleGUI as sg
sg.theme("SystemDefault1")
# sys.path.insert(0, "..")
import sys

# logging modification


class GuiHandler(logging.Handler):
    def __init__(self, multiline_element):
        super().__init__()
        self.multiline_element = multiline_element

    def emit(self, record):
        log_entry = self.format(record)
        self.multiline_element.print(log_entry)


# Main data set used as a template
tagData = {
    "Line1": {
        'Temperature.PV': 18.616,
        'Level.PV': 595.0,
        'Pump1.PV': 0.0,
        'Pump1.CMD': True,
        'Pump1.Speed.SP': 16.37,
        'Pump2.PV': 0.0,
        'Pump2.CMD': False,
        'Pump2.Speed.SP': 11.24,
        'Inlet1.CMD': True,
        'Inlet2.CMD': False,
        'Inlet1.CLS': False,
        'Inlet1.OLS': True,
        'Inlet2.CLS': True,
        'Inlet2.OLS': False,
        'Outlet.CLS': False,
        'Outlet.OLS': False,
        'Agitator.Speed.PV': 3200.0,
        'Agitator.CMD': False,
        'Agitator.PV': 0.0,
        'MixingTime.PV': 25.0,
        'Outlet.CMD': False,
        'Status.STR': "Awaiting status...",
    },
    "Line2": {
        'Temperature.PV': 21.816,
        'Level.PV': 150.0,
        'Pump1.PV': 0.0,
        'Pump1.CMD': True,
        'Pump1.Speed.SP': 16.37,
        'Pump2.PV': 0.0,
        'Pump2.CMD': False,
        'Pump2.Speed.SP': 11.24,
        'Inlet1.CMD': True,
        'Inlet2.CMD': False,
        'Inlet1.CLS': False,
        'Inlet1.OLS': True,
        'Inlet2.CLS': True,
        'Inlet2.OLS': False,
        'Outlet.CLS': False,
        'Outlet.OLS': False,
        'Agitator.Speed.PV': 3200.0,
        'Agitator.CMD': False,
        'Agitator.PV': 0.0,
        'MixingTime.PV': 25.0,
        'Outlet.CMD': False,
        'Status.STR': "Awaiting status...",
    },
    "Line3": {
        'Temperature.PV': 121.816,
        'Level.PV': 820.0,
        'Pump1.PV': 0.0,
        'Pump1.CMD': False,
        'Pump1.Speed.SP': 16.37,
        'Pump2.PV': 0.0,
        'Pump2.CMD': False,
        'Pump2.Speed.SP': 11.24,
        'Inlet1.CMD': False,
        'Inlet2.CMD': False,
        'Inlet1.CLS': True,
        'Inlet1.OLS': False,
        'Inlet2.CLS': True,
        'Inlet2.OLS': False,
        'Outlet.CLS': False,
        'Outlet.OLS': True,
        'Agitator.Speed.PV': 3200.0,
        'Agitator.CMD': False,
        'Agitator.PV': 0.0,
        'MixingTime.PV': 25.0,
        'Outlet.CMD': True,
        'Status.STR': "Awaiting status...",
    },
    "Line4": {
        'Temperature.PV': 17.816,
        'Level.PV': 785.0,
        'Pump1.PV': 0.0,
        'Pump1.CMD': False,
        'Pump1.Speed.SP': 16.37,
        'Pump2.PV': 0.0,
        'Pump2.CMD': True,
        'Pump2.Speed.SP': 11.24,
        'Inlet1.CMD': False,
        'Inlet2.CMD': True,
        'Inlet1.CLS': True,
        'Inlet1.OLS': False,
        'Inlet2.CLS': False,
        'Inlet2.OLS': True,
        'Outlet.CLS': False,
        'Outlet.OLS': False,
        'Agitator.Speed.PV': 3200.0,
        'Agitator.CMD': False,
        'Agitator.PV': 0.0,
        'MixingTime.PV': 25.0,
        'Outlet.CMD': False,
        'Status.STR': "Awaiting status...",
    },
    "Line5": {
        'Temperature.PV': 91.816,
        'Level.PV': 520.0,
        'Pump1.PV': 0.0,
        'Pump1.CMD': False,
        'Pump1.Speed.SP': 16.37,
        'Pump2.PV': 0.0,
        'Pump2.CMD': False,
        'Pump2.Speed.SP': 11.24,
        'Inlet1.CMD': False,
        'Inlet2.CMD': False,
        'Inlet1.CLS': True,
        'Inlet1.OLS': False,
        'Inlet2.CLS': True,
        'Inlet2.OLS': False,
        'Outlet.CLS': False,
        'Outlet.OLS': True,
        'Agitator.Speed.PV': 3200.0,
        'Agitator.CMD': False,
        'Agitator.PV': 0.0,
        'MixingTime.PV': 25.0,
        'Outlet.CMD': True,
        'Status.STR': "Awaiting status...",
    }
}

statusData = {
    "line1Status": {
        'filling': 1,
        'draining': 0,
        'mixing': 0,
        'mixIter': 0
    },
    "line2Status": {
        'filling': 1,
        'draining': 0,
        'mixing': 0,
        'mixIter': 0
    },
    "line3Status": {
        'filling': 0,
        'draining': 1,
        'mixing': 0,
        'mixIter': 0
    },
    "line4Status": {
        'filling': 1,
        'draining': 0,
        'mixing': 0,
        'mixIter': 0
    },
    "line5Status": {
        'filling': 0,
        'draining': 1,
        'mixing': 0,
        'mixIter': 0
    },
}


class OPCUAServer():
    def __init__(self):
        """ initiate global scope """
        
        self.host_name = socket.gethostname()
        self.server_app_uri = f"urn:{self.host_name}::opcua-server1"
        self.cert_user_manager = CertificateUserManager()
        self.server = Server(user_manager=self.cert_user_manager)
        self.idx = None
        self.simulated_data_node = None
        self.num_equipments = 1
        self.equipments = {}
        self.statuses = ["line1Status", "line2Status",
                         "line3Status", "line4Status", "line5Status"]
        self.mixIter = 0
        self.step = 0
        self.Lines = list()
        self.serverLive = True
        self.custom_enabled = False
        self.custom_equipment = {}
        self.custom_config = []
        self.clients_configured = 0
        self.userID = 1
        self.layout = None
        self.certGen = CertGen(self.host_name)

        

    async def configure(self):
        """ general configuration """
        await self.addUsers()
        await self.server.init()
        await self.server.set_application_uri(self.server_app_uri)
        port = '4840'
        # change = input("Do you want to change default port? (y/n): ")
        # set timer to 3 dots
        change = False
        ###
        if change == 'y' or change == 'Y':
            port = input('Enter port number: ')
        self.endpoint = f"opc.tcp://{self.host_name}:{port}/opcua-server1"
        self.server.set_endpoint(self.endpoint)
        # print(f"\n\t -- Connection URL: {self.endpoint} --\n")
        self.server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt],
                                        permission_ruleset=SimpleRoleRuleset())
        
        await self.checkCerts()

        #print("After validating")

        await self.server.load_certificate(str(self.server_cert))
        await self.server.load_private_key(str(self.server_private_key))
        validator = CertificateValidator(
            options=CertificateValidatorOptions.EXT_VALIDATION | CertificateValidatorOptions.PEER_CLIENT)
        self.server.set_certificate_validator(validator)


        uri = f"{self.host_name}/PLANT"
        self.idx = await self.server.register_namespace(uri)
        self.objects = self.server.get_objects_node()
        # add_object(self.idx, "PLC1")
        self.simulated_data_node = await self.objects.add_object(ua.NodeId("Production", self.idx), "Production")

    async def checkCerts(self):
        # Certificates loading and check - block if fail
        # check if they are there before calling
        self.server_cert = Path("certificates/certs/myserver-selfsigned.der")
        self.server_private_key = Path("certificates/private/myserver.pem")
        try:
            await self.server.load_certificate(str(self.server_cert))
            await self.server.load_private_key(str(self.server_private_key))
        except FileNotFoundError:
            # self.serverLive = False
            await self.certWindow()
            #print("no crets folder")
            #input("Click on me...")
            #await self.certGen.generateCerts()
            await asyncio.sleep(2)

    async def addUsers(self):
        """ add users and their certificates """
        self.userID = 0
        self.clients_configured = 0
        try:
            all = listdir("certificates/clients")
            try:
                self.logServer.print("\nReloading all Client Certificates....")
            except AttributeError:
                pass
            for user in all:
                try:
                    self.logServer.print(f"Added: {user}")
                except AttributeError:
                    pass
                await self.cert_user_manager.add_admin(f"certificates/clients/{user}", name=f"user{self.userID}")
                self.userID += 1
                self.clients_configured += 1
        except FileNotFoundError:
                pass
            

    async def createTags(self):
        for equipment_name in tagData:
            self.equipments[equipment_name] = await self.create_equipment_node(self.simulated_data_node, equipment_name, self.idx)
            # this ideally should be refactored to allow global object variable creation instead of condition statement
            if equipment_name == "Line1":
                self.Line1 = self.equipments[equipment_name]
                self.Lines.append(self.Line1)
            elif equipment_name == "Line2":
                self.Line2 = self.equipments[equipment_name]
                self.Lines.append(self.Line2)
            elif equipment_name == "Line3":
                self.Line3 = self.equipments[equipment_name]
                self.Lines.append(self.Line3)
            elif equipment_name == "Line4":
                self.Line2 = self.equipments[equipment_name]
                self.Lines.append(self.Line2)
            elif equipment_name == "Line5":
                self.Line3 = self.equipments[equipment_name]
                self.Lines.append(self.Line3)

        # Code below was used to allow custom tags to be loaded via CSV file.
        # I do think that if this functionality is needed ,it should be implemented without simulation for Lines for better error handling

        # csvList = self.checkCSV()
        # for name in csvList:
        #     custom_equipment = name
        #     custom = self.loadCustom(custom_equipment)
        #     if custom:
        #         self.custom_enabled = True
        #         self.equipments[custom_equipment] = await self.create_equipment_node(self.simulated_data_node, custom_equipment, self.idx)
        #         self.custom_equipment.update(self.equipments[name])
                # print(f"Custom {name}.csv loaded ...OK")

    # def checkCSV(self):
    #     filesToProcess = []
    #     files = listdir(getcwd())
    #     for file in files:
    #         if file[-3:] == 'csv' or file[-3:] == 'CSV':
    #                 filesToProcess.append(file[:-4])
    #     return filesToProcess

    # def loadCustom(self, name):
    #     csv_file = f"{name}.csv"
    #     if not path.isfile(csv_file):
    #         #print(" No custom tags found\n")
    #         pass
    #     else:
    #         tagData[name] = {}
    #         with open(csv_file) as file:
    #             csvFile = reader(file)
    #             for row in csvFile:
    #                 if 'tagname' in row:
    #                     pass
    #                 else:
    #                     self.custom_config.append(row)
    #                     if row[0][-3:] == 'CMD':
    #                         if row[1] == 'True':
    #                             tagData[name][row[0]] = True
    #                         elif row[1] == 'False':
    #                             tagData[name][row[0]] = False
    #                     elif row[0][-2:] in ['PV', 'SP']:
    #                         tagData[name][row[0]] = float(row[1])
    #                     elif row[0][-3:] == 'STR':
    #                         tagData[name][row[0]] = row[1]
    #                     else:
    #                         tagData[name][row[0]] = int(row[1])
    #             return True

    async def create_equipment_node(self, parent_node, equipment_name, namespace_idx):
        equipment_node = await parent_node.add_object(ua.NodeId("Production." + equipment_name, namespace_idx), equipment_name)
        tags = {}
        for tag_name in tagData[equipment_name].keys():
            if tag_name[-2:] == "PV" or tag_name[-2:] == "SP":
                # tags[tag_name] = await equipment_node.add_variable(namespace_idx, tag_name, 0, ua.VariantType.Double)
                tags[tag_name] = await equipment_node.add_variable(ua.NodeId(f"Production.{equipment_name}.{tag_name}", namespace_idx), tag_name, 0, ua.VariantType.Double)
            elif tag_name[-3:] in ["CMD", "OLS", "CLS"] or tag_name[-8:] == "Position":
                # tags[tag_name] = await equipment_node.add_variable(namespace_idx, tag_name, 0, ua.VariantType.Boolean)
                tags[tag_name] = await equipment_node.add_variable(ua.NodeId(f"Production.{equipment_name}.{tag_name}", namespace_idx), tag_name, 0, ua.VariantType.Boolean)
            elif tag_name[-3:] == "STR":
                # tags[tag_name] = await equipment_node.add_variable(namespace_idx, tag_name, 0, ua.VariantType.String)
                tags[tag_name] = await equipment_node.add_variable(ua.NodeId(f"Production.{equipment_name}.{tag_name}", namespace_idx), tag_name, 0, ua.VariantType.String)
            else:
                # tags[tag_name] = await equipment_node.add_variable(namespace_idx, tag_name, 0, ua.VariantType.Int64)
                tags[tag_name] = await equipment_node.add_variable(ua.NodeId(f"Production.{equipment_name}.{tag_name}", namespace_idx), tag_name, 0, ua.VariantType.Int64)
        return tags

    async def initTags(self):
        for equipment_name, tags in self.equipments.items():
            for tag_name, value in tagData[equipment_name].items():
                # print(f"Tag: {tag_name} , {value}")
                await tags[tag_name].set_value(value)
                if tag_name[-3:] == "CMD" or tag_name[-2:] == "SP":
                    await tags[tag_name].set_writable()

    def window_layout(self):
        """ GUI window configuration """
        logBoxSize = (100, 11)
        btnSize = (10, 2)
        logFramesSize = (217, 30)
        connection_frame = [[sg.Text(f"Hostname: {self.host_name}   PORT: 4840"), sg.Text(
            " "*6), sg.Text(f"Connection URL: "), sg.Input(default_text=f"{self.endpoint}", expand_x=True)],]
        self.logServer = sg.Multiline(
            size=logBoxSize, font=('Courier', 8), key='-LOG-')
        stepCount = [[sg.Text('Current Step: '), sg.Text('0', key='STEP')]]
        clientCount = [[sg.Text('Connected clients: '), sg.Text(
            '0', key='CLIENT', text_color="green")]]
        allowedClients = [
            [sg.Text(f"Allowed clients: "), sg.Text(f"{self.clients_configured}", key='ALLOWED')]]
        server_layout = [[self.logServer]]
        self.layout = [
            [sg.Frame('SERVER - DETAILS', connection_frame, expand_x=True)],
            [sg.Frame('SERVER - LOG', server_layout, expand_x=True)],
            [sg.Frame('', stepCount, size=logFramesSize), sg.Frame('', clientCount, size=logFramesSize),
             sg.Frame('', allowedClients, size=logFramesSize)],
            [sg.Button('Exit', size=btnSize),sg.Push() , sg.Button('Reload Certifcates', size=(20, 2)),]
        ]
        self.window = sg.Window('OPCUA Production Lines V4', self.layout, size=(
            700, 340), icon='SOLPTico.ico', finalize=True)
        
    async def certWindow(self):
        btnSize = (10, 2)
        today = datetime.today()
        year_later = today + timedelta(days=365)


        info = [
            [sg.Text(f"""            You will now generate self-signed certifiates for this machine.
            Newly created certificates folder will contain all the certificates neccesary in order
            for encryption to be allowed. Certificate for this OPCUA server will be located in the
            file path below. Install certificate to this machine by executing it and add it to 
            the Trusted Root Certificates.
            NOTE: Certificates will be valid till the end of:  {year_later.strftime("%d-%m-%Y")}

            File path: /certificates/certs/myserver-selfsingned.crt
            """)],           
            ]

        auth = [
            [sg.Text(f"""            Basic256Sha256 - Sign & Encrypt
            To allow client connection to this OPCUA server, copy client certificates to folder below.
                     
            Folder: /certificates/clients
            """)],           
            ]
        hostDetails = [[sg.Text(f"            Hostname: {self.host_name} \n            IP Address: {socket.gethostbyname(self.host_name)}")]]

        layout2 = [ 
                    [sg.Frame('INFORMATION', info, expand_x=True)],
                    [sg.Frame('CLIENT AUTHENTICATION', auth, expand_x=True)],
                    [sg.Frame('SERVER - DETAILS', hostDetails, size=(250, 70))],
                    [sg.Text("")],
                    #[sg.Text(f"OPCUA Server will start \nafter generating certificates")],
                    [sg.Button('Generate Certificates', size=(20, 2)), sg.Push() ,sg.Button('EXIT', size=btnSize)] ]

        # Create the Window
        window2 = sg.Window('OPCUA Production Lines - Certificates Generator', layout2, size=(
            630, 460), icon='SOLPTico.ico')
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window2.read()
            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'EXIT':
                # nuclear stop , not very elegant would do with changing this
                sys.exit()
                break

            if event == 'Generate Certificates':
                await self.certGen.generateCerts()
                window2.close()
                #self.serverLive = True
                break

    def loggingService(self):
        """ modified logger module to print to a multiline gui window """
        self.logger = logging.getLogger("asyncua")
        self.logger.setLevel(logging.WARNING)  # Set the logging level
        log_element = self.window['-LOG-']
        self.gui_handler = GuiHandler(log_element)
        self.logger.addHandler(self.gui_handler)
        for handler in self.logger.handlers[:]:
            if not isinstance(handler, GuiHandler):
                self.logger.removeHandler(handler)

    async def main(self):
        """ Program Main loop """
        
        await self.configure()
        await self.createTags()
        await self.initTags()
        counter = 0
        statusMsg = True
        # inintiate GUI
        self.window_layout()
        self.loggingService()

        async with self.server:
            while self.serverLive:
                event, values = self.window.read(timeout=100)
                if event == sg.WIN_CLOSED or event == 'Exit':
                    break
                try:
                    if counter > 10:
                        await self.runSim()
                        current_connections = getattr(
                            self.server.iserver.isession, "_current_connections", 0)
                        self.window['CLIENT'].update(current_connections)
                        if statusMsg:
                            self.logServer.print("OPCUA Server Status: Running...")
                            statusMsg = False
                        # not enabled in this version
                        # if self.custom_enabled:
                        #     await self.runCustom()
                        # ---------------------------
                    else:
                        counter += 1
                except Exception as e:
                    self.logServer.print(f"Error: {e}")

                if event == "Reload Certifcates":
                    try:
                        await self.addUsers()
                    except Exception as e:
                        self.logServer.print(f"Error: {e}")
                    self.window['ALLOWED'].update(self.clients_configured)
                await asyncio.sleep(0.1)
        self.window.close()

    async def runCustom(self):
        """ custom tags logic not implemented in this version. """
        for tag in self.custom_config:
            if tag[0][-2:] == 'PV' and tag[3] == 'True':
                if f"{tag[0][:-3]}.CMD" in self.custom_equipment.keys():
                    if await self.custom_equipment[f"{tag[0][:-3]}.CMD"].get_value():
                        await self.custom_equipment[tag[0]].set_value(uniform(float(tag[1]), float(tag[2])))
                    else:
                        await self.custom_equipment[tag[0]].set_value(0.0)
                else:
                    await self.custom_equipment[tag[0]].set_value(uniform(float(tag[1]), float(tag[2])))

    async def runSim(self):
        """ update values on every iteration """
        # print couter to GUI
        self.window['STEP'].update(self.step)
        if self.step == 3_024_000:
            self.step = 0
        self.step += 1


        for i in range(len(self.Lines)):
            await self.runLine(self.Lines[i], self.statuses[i])

    async def runLine(self, line, status):
        if statusData[status]["filling"]:
            if await line["Status.STR"].get_value() != "Filling":
                await line["Status.STR"].set_value("Filling")
            await self.fillTank(line, status)
        if not statusData[status]["filling"] and not statusData[status]["draining"]:
            if await line["Status.STR"].get_value() != "Mixing":
                await line["Status.STR"].set_value("Mixing")
            await self.mixTank(line, status)
        if statusData[status]["draining"]:
            if await line["Status.STR"].get_value() != "Draining":
                await line["Status.STR"].set_value("Draining")
            await self.drainTank(line, status)

    async def fillTank(self, line, status):
        if 0 <= await line["Level.PV"].get_value() < 600 and await line["Inlet1.CMD"].get_value() and await line["Pump1.CMD"].get_value():
            await line['Pump1.PV'].set_value(uniform(await line["Pump1.Speed.SP"].get_value() - 1, await line["Pump1.Speed.SP"].get_value() + 1))
            await line["Level.PV"].set_value(await line["Level.PV"].get_value() + await line["Pump1.Speed.SP"].get_value()/10)
            if await line["Temperature.PV"].get_value() > 18.816:
                await line["Temperature.PV"].set_value(await line["Temperature.PV"].get_value() - 0.38)
            else:
                await line["Temperature.PV"].set_value(uniform(17.6, 18.4))

        if 600 < await line["Level.PV"].get_value() < 658:
            await line["Inlet1.CMD"].set_value(False)
            await line["Pump1.CMD"].set_value(False)
            await line['Pump1.PV'].set_value(0.0)
            await line["Inlet2.CMD"].set_value(True)
            await line["Pump2.CMD"].set_value(True)

        if 600 <= await line["Level.PV"].get_value() < 900 and await line["Inlet2.CMD"].get_value() and await line["Pump2.CMD"].get_value():
            await line['Pump2.PV'].set_value(uniform(await line["Pump2.Speed.SP"].get_value() - 1, await line["Pump2.Speed.SP"].get_value() + 1))
            await line["Level.PV"].set_value(await line["Level.PV"].get_value() + await line["Pump2.Speed.SP"].get_value()/10)
            if await line["Level.PV"].get_value() > 900:
                await line["Level.PV"].set_value(900.0)
            await line["Temperature.PV"].set_value(uniform(17.6, 18.4))

        if await line["Level.PV"].get_value() >= 900:
            await line["Inlet2.CMD"].set_value(False)
            await line["Agitator.CMD"].set_value(True)
            await line["Pump2.CMD"].set_value(False)
            await line['Pump2.PV'].set_value(0.0)
            statusData[status]["filling"] = 0
            statusData[status]["mixing"] = 1

        if await line["Inlet1.CMD"].get_value() == True:
            await line["Inlet1.OLS"].set_value(True)
            await line["Inlet1.CLS"].set_value(False)
        else:
            await line["Inlet1.OLS"].set_value(False)
            await line["Inlet1.CLS"].set_value(True)
            await line["Pump1.PV"].set_value(0.0)

        if await line["Inlet2.CMD"].get_value() == True:
            await line["Inlet2.OLS"].set_value(True)
            await line["Inlet2.CLS"].set_value(False)
        else:
            await line["Inlet2.OLS"].set_value(False)
            await line["Inlet2.CLS"].set_value(True)
            await line["Pump2.PV"].set_value(0.0)

        if await line["Pump1.CMD"].get_value() == False:
            await line["Pump1.PV"].set_value(0.0)
        if await line["Pump2.CMD"].get_value() == False:
            await line["Pump2.PV"].set_value(0.0)

    async def mixTank(self, line, status):
        if statusData[status]["mixing"] and await line["Agitator.CMD"].get_value():
            await line['Agitator.PV'].set_value(uniform(await line["Agitator.Speed.PV"].get_value() - 10, await line["Agitator.Speed.PV"].get_value() + 10))
            await line["Level.PV"].set_value(uniform(896.0, 909.0))
            if await line["Temperature.PV"].get_value() <= 130:
                await line["Temperature.PV"].set_value(await line["Temperature.PV"].get_value() + 0.76)
            elif await line["Temperature.PV"].get_value() > 130:
                await line["Temperature.PV"].set_value(uniform(131.6, 134.1))
        statusData[status]["mixIter"] += 0.1

        if round(statusData[status]["mixIter"], 2) == await line['MixingTime.PV'].get_value():
            statusData[status]["mixIter"] = 0
            statusData[status]["mixing"] = 0
            await line["Agitator.CMD"].set_value(False)
            await line["Agitator.PV"].set_value(0.0)
            statusData[status]["draining"] = 1
            await line["Outlet.CMD"].set_value(True)

    async def drainTank(self, line, status):
        if await line["Level.PV"].get_value() > 0 and await line["Outlet.CMD"].get_value():
            await line["Level.PV"].set_value(await line["Level.PV"].get_value() - 2.606)
            if await line["Level.PV"].get_value() < 0:
                await line["Level.PV"].set_value(0.0)
            if await line["Temperature.PV"].get_value() > 21.816 and await line["Level.PV"].get_value() >= 620:
                await line["Temperature.PV"].set_value(await line["Temperature.PV"].get_value() - 0.08)
            elif await line["Temperature.PV"].get_value() > 21.816 and await line["Level.PV"].get_value() < 620:
                await line["Temperature.PV"].set_value(await line["Temperature.PV"].get_value() - 0.23)
                if await line["Temperature.PV"].get_value() < 21.816:
                    await line["Temperature.PV"].set_value(21.816)

        if await line["Level.PV"].get_value() == 0:
            await line["Outlet.CMD"].set_value(False)
            statusData[status]["draining"] = 0
            statusData[status]["filling"] = 1
            await line["Inlet1.CMD"].set_value(True)
            await line["Pump1.CMD"].set_value(True)
        if await line["Outlet.CMD"].get_value() == True:
            await line["Outlet.OLS"].set_value(True)
        else:
            await line["Outlet.CLS"].set_value(False)


class CertGen():
    def __init__(self, myHostName) -> None:
        self.HOSTNAME = myHostName
        # used for subject common part
        self.NAMES = {
            'countryName': 'UK',
            'stateOrProvinceName': 'NW',
            'localityName': 'Cheadle',
            'organizationName': "SolutionsPT",
        }

        self.CLIENT_SERVER_USE = [ExtendedKeyUsageOID.CLIENT_AUTH,
                                  ExtendedKeyUsageOID.SERVER_AUTH]
        
    async def _createFolders(self):
        # setup the paths for the certs, keys and csr
        self.base = Path('certificates')
        self.base_csr: Path = self.base / 'csr'
        self.base_private: Path = self.base / 'private'
        self.base_certs: Path = self.base / 'certs'
        self.base_clients: Path = self.base / 'clients'
        self.base_csr.mkdir(parents=True, exist_ok=True)
        self.base_private.mkdir(parents=True, exist_ok=True)
        self.base_certs.mkdir(parents=True, exist_ok=True)
        self.base_clients.mkdir(parents=True, exist_ok=True)

    def generate_private_key_for_myserver(self):
        key: RSAPrivateKey = generate_private_key()
        key_file = self.base_private / "myserver.pem"
        key_file.write_bytes(dump_private_key_as_pem(key))

    async def generate_self_signed_certificate(self):
        subject_alt_names: List[x509.GeneralName] = [x509.UniformResourceIdentifier(f"urn:{self.HOSTNAME}::opcua-server1"),
                                                     x509.DNSName(f"{self.HOSTNAME}")]
        # key: RSAPrivateKey = generate_private_key()
        key = await load_private_key(self.base_private / "myserver.pem")

        cert: x509.Certificate = generate_self_signed_app_certificate(key,
                                                                      f"opcua-server1@{self.HOSTNAME}",
                                                                      self.NAMES,
                                                                      subject_alt_names,
                                                                      extended=self.CLIENT_SERVER_USE)
        cert_file = self.base_certs / "myserver-selfsigned.der"
        cert_file.write_bytes(cert.public_bytes(encoding=Encoding.DER))

    def generate_applicationgroup_ca(self):
        subject_alt_names: List[x509.GeneralName] = [x509.UniformResourceIdentifier(f"urn:{self.HOSTNAME}::opcua-server1"),
                                                     x509.DNSName(f"{self.HOSTNAME}")]
        key: RSAPrivateKey = generate_private_key()
        cert: x509.Certificate = generate_self_signed_app_certificate(key,
                                                                      "SolutionsPT",
                                                                      self.NAMES,
                                                                      subject_alt_names,
                                                                      extended=[])
        key_file = self.base_private / 'ca_application.pem'
        cert_file = self.base_certs / 'ca_application.der'
        key_file.write_bytes(dump_private_key_as_pem(key))
        cert_file.write_bytes(cert.public_bytes(encoding=Encoding.DER))

    async def generate_csr(self):
        subject_alt_names: List[x509.GeneralName] = [x509.UniformResourceIdentifier(f"urn:{self.HOSTNAME}::opcua-server1"),
                                                     x509.DNSName(f"{self.HOSTNAME}")]
        key: RSAPrivateKey = generate_private_key()
        key = await load_private_key(self.base_private / 'myserver.pem')

        csr: x509.CertificateSigningRequest = generate_app_certificate_signing_request(key,
                                                                                       f"opcua-server1@{self.HOSTNAME}",
                                                                                       self.NAMES,
                                                                                       subject_alt_names,
                                                                                       extended=self.CLIENT_SERVER_USE)
        # key_file = self.base_private / 'myserver.pem'
        csr_file = self.base_csr / 'myserver.csr'
        # key_file.write_bytes(dump_private_key_as_pem(key))
        csr_file.write_bytes(csr.public_bytes(encoding=Encoding.PEM))

    async def sign_csr(self):
        issuer = await load_certificate(self.base_certs / 'ca_application.der')
        key_ca = await load_private_key(self.base_private / 'ca_application.pem')
        csr_file: Path = self.base_csr / 'myserver.csr'
        csr = x509.load_pem_x509_csr(csr_file.read_bytes())
        cert: x509.Certificate = sign_certificate_request(
            csr, issuer, key_ca, days=30)
        (self.base_certs / 'myserver.der').write_bytes(cert.public_bytes(encoding=Encoding.DER))

    async def generateCerts(self):
        await self._createFolders()
        # create key and reuse it for self_signed and generate_csr
        self.generate_private_key_for_myserver()
        # generate self signed certificate for myserver-selfsigned
        await self.generate_self_signed_certificate()
        # generate certificate signing request and sign it with the ca for myserver
        self.generate_applicationgroup_ca()
        await self.generate_csr()
        await self.sign_csr()
        #print("SSL All done")


async def main():
    server = OPCUAServer()
    # Initialize
    gui_task = asyncio.create_task(server.main())
    await asyncio.gather(gui_task)

if __name__ == "__main__":
    asyncio.run(main())
