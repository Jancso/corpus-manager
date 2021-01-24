""""Reads session and speaker metadata from a tabular format and converts them to one IMDI (as defined in the CMDI framework) per session."

Input (default locations; execute python3 IMDIMaker.py --help for help on how to set different locations):
../Metadata/sessions.csv
../Metadata/participants.csv
../Metadata/files.csv
../Workflow/monitor.csv
../Metadata/IMDI/
../Metadata/Dene_IMDI.ini

Output:
../Metadata/IMDI/<imdi file>
./imdi.log

If the flag '-v' is set, then all XMLs will be created in the IMDI version 1.2.

Example:
    python3 IMDIMaker.py
"""


import re
import os
import sys
import csv
import time
import logging
import argparse
import datetime
import configparser
from collections import defaultdict
from lxml.etree import *


def commandline_setup():
    """Set up command line arguments"""
    parser = argparse.ArgumentParser(description="Specify paths for metadata files.")
    parser.add_argument("-s", "--sessions", help="path to sessions.csv", default="../Metadata/sessions.csv")
    parser.add_argument("-p", "--participants", help="path to participants.csv", default="../Metadata/participants.csv")
    parser.add_argument("-f", "--files", help="path to files.csv", default="../Metadata/files.csv")
    parser.add_argument("-m", "--monitor", help="path to monitor.csv", default="../Workflow/monitor.csv")
    parser.add_argument("-i", "--imdi", help="path for IMDI file", default="../Metadata/IMDI/")
    parser.add_argument("-d", "--ini", help="path to Dene.ini", default="../Metadata/Dene_IMDI.ini")
    parser.add_argument("-v", "--new-version", help="create file(s) in IMDI 1.2", action="store_true")

    return parser.parse_args()


class IMDIMaker:
    """Generate CMDI files of profile IMDI for dene"""

    def __init__(self):
        """Intialize variables for metadata files"""
        # get parsed arguments
        self.args = commandline_setup()
        # get logger to track errors while creating the IMDI files
        self.logger = self.get_logger()

        # load Dene.ini where all the fixed values are stored
        self.config = configparser.ConfigParser()
        # preserve case
        self.config.optionxform = str
        if not self.config.read(self.args.ini):
            print("Couldn't find Dene_IMDI.ini at", self.args.ini)
            sys.exit(1)

        # intialize variables storing metadata
        self.session_metadata = {}
        self.participants = {}
        self.resources = defaultdict(list)

        # create IMDI directory if does not already exist
        if not os.path.isdir(self.args.imdi):
            try:
                os.mkdir(self.args.imdi)
            except FileNotFoundError:
                print("Folder IMDI couldn't be created at", self.args.imdi)
                sys.exit(1)


    def get_logger(self):
        """Produce logs if some of the elements cannot be created"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler("imdi.log", mode="w")
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(funcName)s|%(levelname)s|%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger


    def generate_imdis(self):
        """Generate IMDI's for all sessions from session.csv"""
        try:
            # open sessions.csv for reading
            sessions_file = open(self.args.sessions, "r")
        except FileNotFoundError:
            print("Couldn't find sessions.csv at", self.args.sessions)
            sys.exit(1)
        else:
            # get and store metadata of all participants and files
            self.get_participants()
            self.get_files()

            for session in csv.DictReader(sessions_file):

                # store metadata of this session
                self.session_metadata = session

                # TODO: make this more corpus-independent
                # extract and add shortname since it is needed several times
                match = re.search(r"deslas-([A-Z]{3})", self.session_metadata["Code"])
                if match:
                    self.session_metadata["Short name"] = match.group(1)
                else:
                    self.logger.error(
                        "Short name could not be extracted from {}".format(
                            self.session_metadata["Code"]))
                    continue

                # check in which IMDI version the file should be created
                if self.args.new_version:
                    # IMDI 1.2
                    self.create_session()
                else:
                    # IMDI 1.1
                    self.create_cmd()


    def create_cmd(self):
        """Create CMDI element 'CMD'"""

        # set namespace
        clarin_ns = "http://www.clarin.eu/cmd/"
        clarin = "{%s}" % clarin_ns
        NSMAP = {None : clarin_ns}

        # create root element
        cmd_element = Element(clarin + "CMD", nsmap=NSMAP, CMDVersion="1.1")

        self.create_header(cmd_element)
        self.create_cmd_resources(cmd_element)
        components_element = SubElement(cmd_element, "Components")
        self.create_session(components_element)

        # write to file
        self.write_file(cmd_element)


    def create_header(self, cmd_element):
        """Create CMDI element 'Header'"""
        header_element = SubElement(cmd_element, "Header")

        for key, value in [
            ("MdCreator", sys.argv[0]),
            ("MdCreationDate", time.strftime("%Y-%m-%d")),
            ("MdSelfLink", self.config["CMD"]["MdSelfLink"] + self.session_metadata["Code"] + ".imdi"),
            ("MdProfile", self.config["CMD"]["MdProfile"]),
            ("MdCollectionDisplayName", self.config["CMD"]["MdCollectionDisplayName"])
            ]:

            SubElement(header_element, key).text = value


    def create_cmd_resources(self, cmd_element):
        """Create CMDI element 'Resources'"""
        resources_element = SubElement(cmd_element, "Resources")
        resource_proxy_list_element = SubElement(resources_element, "ResourceProxyList")

        for resource_proxy_element, resource_element in self.resources[self.session_metadata["Code"]]:
            resource_proxy_list_element.append(resource_proxy_element)

        journal_file_proxy_list_element = SubElement(resources_element, "JournalFileProxyList")
        resource_relation_list_element = SubElement(resources_element, "ResourceRelationList")


    def create_session(self, components_element=None):
        """Creates CMDI element 'Components'"""
        if self.args.new_version:
            session_element = Element("Session")
        else:
            session_element = SubElement(components_element, "Session")

        for key, value in [
            ("Name", self.session_metadata["Code"]),
            ("Title", self.get_title()),
            ("Date", self.session_metadata["Date"].replace(".", "-"))
            ]:

            SubElement(session_element, key).text = value

        if self.session_metadata["Situation"]:
            descriptions_element = SubElement(session_element, "descriptions")
            SubElement(descriptions_element, "Description",
                LanguageId=self.config["LanguageId"]["Description"]).text = self.session_metadata["Situation"]

        self.create_mdgroup(session_element)
        self.create_session_resources(session_element)

        if self.args.new_version:
            # write to file
            self.write_file(session_element)


    def write_file(self, element):
        """Write XML to file"""
        # set path for IMDI file
        path = os.path.join(self.args.imdi, self.session_metadata["Code"] + ".imdi")

        # write XML to this file
        ElementTree(element).write(path, pretty_print=True, encoding="utf-8", xml_declaration=True)

        print(self.session_metadata["Code"])


    def get_title(self):
        """Get title for a certain session"""
        # initial part of title
        title = " session of target child " + self.session_metadata["Short name"] + " on " + self.session_metadata["Date"]
        # regex to extract number of a session code
        match = re.search(r"-\d\d-\d\d-(\d)[A-Z]*", self.session_metadata["Code"])
        # if there is number, get its ordinal and concatenate to title, otherwise concatenate 'only'
        if match:
            # function to get ordinal from a number: http://stackoverflow.com/questions/9647202/ordinal-numbers-replacement#answer6
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            title = ordinal(int(match.group(1))) + title
        else:
            title = "only" + title

        return title


    def create_mdgroup(self, session_element):
        """Create IMDI element 'MDGroup'"""
        mdgroup_element = SubElement(session_element, "MDGroup")
        self.create_location(mdgroup_element)
        self.create_project(mdgroup_element)

        keys_element = SubElement(mdgroup_element, "Keys")
        SubElement(keys_element, "Key", Name="Duration").text = self.session_metadata["Length of recording"]

        self.create_content(mdgroup_element)
        self.create_actors(mdgroup_element)


    def create_location(self, mdgroup_element):
        """Create IMDI element 'Location'"""
        location_element = SubElement(mdgroup_element, "Location")

        for field in ["Continent", "Country", "Region"]:
            SubElement(location_element, field).text = self.config["Location"][field]

        SubElement(location_element, "Address").text = self.session_metadata["Location"]


    def create_project(self, mdgroup_element):
        """Create IMDI element 'Project'"""
        project_element = SubElement(mdgroup_element, "Project")

        for field in ["Name", "Title", "Id"]:
            SubElement(project_element, field).text = self.config["Project"][field]

        contact_element = SubElement(project_element, "Contact")
        for key, value in self.config.items("Contact"):
            SubElement(contact_element, key).text = value

        descriptions_element = SubElement(project_element, "descriptions")
        SubElement(descriptions_element, "Description",
            LanguageId=self.config["LanguageId"]["Description"]).text = self.config["Project"]["descriptions"]


    def create_content(self, mdgroup_element):
        """Create IMDI element 'Content'"""
        content_element = SubElement(mdgroup_element, "Content")

        for key, value in self.config.items("Content"):
            SubElement(content_element, key).text = value

        context_element = SubElement(content_element, "CommunicationContext")

        for key, value in self.config.items("CommunicationContext"):
            SubElement(context_element, key).text = value

        content_languages_element = SubElement(content_element, "Content_Languages")

        for language in self.config["Languages"]:
            content_language_element = SubElement(content_languages_element, "Content_Language")
            for key, value in self.config.items(language):
                SubElement(content_language_element, key).text = value

        SubElement(content_element, "Keys")

        if self.session_metadata["Content"]:
            descriptions_element = SubElement(content_element, "descriptions")
            SubElement(descriptions_element, "Description",
                LanguageId=self.config["LanguageId"]["Description"]).text = self.session_metadata["Content"]


    def create_actors(self, mdgroup_element):
        """Create IMDI element 'Actors'"""
        actors_element = SubElement(mdgroup_element, "Actors")

        for actor in self.session_metadata["Participants and roles"].split(", "):

            # extract role and short name for this actor
            try:
                shortname, role = re.split(r" (?=\()", actor)
            except ValueError:
                self.logger.error("Element 'Actor' for '" + actor + "' could not be created => format of 'Participants and roles not right'" +
                    "|" + self.session_metadata["Code"])
                continue

            # strip the braces around the role
            role = role[1:-1]

            # get the right actor element
            try:
                actor_element = self.participants[shortname]
            except KeyError:
                self.logger.error("Element 'Actor' for '" + shortname + "' could not be created => short name missing in participants.csv" +
                    "|" + self.session_metadata["Code"])
                continue

            # modify the fields whose values depend on the role of an actor
            if role == "researcher":
                # change 'Role' element
                actor_element[0].text = role
                # change 'FamilySocialRole' element
                actor_element[4].text = "Not-related"
                # change 'EthnicGroup' element
                actor_element[5].text = "German"

            elif role == "recorder":
                actor_element[0].text = role
                actor_element[4].text = "Not-related"
                actor_element[5].text = "Unknown"

            else:
                actor_element[0].text = "Speaker"
                actor_element[4].text = role
                actor_element[5].text = "Dene"

            # try to parse birth date of this actor
            for format in ["%Y-%m-%d", "%Y"]:
                try:
                    birthdate = datetime.datetime.strptime(actor_element[7].text, format)
                except ValueError:
                    birthdate = None
                else:
                    break

            # try to parse date of this session
            try:
                recording_date = datetime.datetime.strptime(self.session_metadata["Date"], "%Y-%m-%d")
            except ValueError:
                recording_date = None

            # if both birth date and recording date could be parsed
            if birthdate and recording_date:
                # then calculate age of this actor at this session
                actor_element[6].text = str(int(abs((recording_date - birthdate).days) / 365))

            # finally add the actor element
            actors_element.append(actor_element)


    def create_session_resources(self, session_element):
        """Create IMDI element 'Resources'"""
        resources_element = SubElement(session_element, "Resources")

        for resource_proxy_element, resource_element in self.resources[self.session_metadata["Code"]]:
            resources_element.append(resource_element)


    def get_participants(self):
        """Get all metadata of the partcipants from participants.csv"""
        try:
            # open participants.csv for reading
            participants_file = open(self.args.participants, "r")
        except FileNotFoundError:
            print("Couldn't find participants.csv at", self.args.participants)
            sys.exit(1)
        else:
            # go through each participant
            for participant in csv.DictReader(participants_file):

                actor_element = Element("Actor")

                for key, value in [
                    ("Role", ""),
                    ("Name", participant["Full name"].split(" ")[0]),
                    ("FullName", participant["Full name"]),
                    ("Code", participant["Short name"]),
                    ("FamilySocialRole", ""),
                    ("EthnicGroup", ""),
                    ("Age", ""),
                    ("BirthDate", participant["Birth date"]),
                    ("Sex", participant["Gender"]),
                    ("Education", participant["Education"]),
                    ("Anonymized", "false")
                    ]:

                    if value:
                        SubElement(actor_element, key).text = value
                    else:
                        SubElement(actor_element, key).text = "Unspecified"

                # only create contact if there is also data available for this actor
                if participant["Contact address"] or "@" in participant["E-mail/Phone"]:
                    contact_element = SubElement(actor_element, "Contact")
                    SubElement(contact_element, "Name").text = participant["Full name"]

                    if participant["Contact address"]:
                        SubElement(contact_element, "Address").text = participant["Contact address"]
                    # do not create this element if phone number is given
                    if "@" in participant["E-mail/Phone"]:
                        SubElement(contact_element, "Email").text = participant["E-mail/Phone"]

                SubElement(actor_element, "Keys")

                if participant["Description"]:
                    descriptions_element = SubElement(actor_element, "descriptions")
                    SubElement(descriptions_element, "Description",
                        LanguageId=self.config["LanguageId"]["Description"]).text = participant["Description"]

                actor_languages_element = SubElement(actor_element, "Actor_Languages")

                if participant["Language biography"]:
                    descriptions_element = SubElement(actor_languages_element, "descriptions")
                    SubElement(descriptions_element, "Description",
                        LanguageId=self.config["LanguageId"]["Description"]).text = participant["Language biography"]

                # first collect the languages the actor speaks
                actor_languages = set()
                for field in ["First languages", "Second languages", "Main language"]:
                    if participant[field]:
                        # split at slash in case two languages are given in a field
                        for language in participant[field].split("/"):
                            actor_languages.add(language)

                # then create an 'Actor_Language' element for each language spoken by this actor
                for actor_language in actor_languages:
                    actor_language_element = SubElement(actor_languages_element, "Actor_Language")

                    # try to get the language data from Dene.ini
                    try:
                        SubElement(actor_language_element, "Id").text = self.config[actor_language]["Id"]
                        SubElement(actor_language_element, "Name").text = self.config[actor_language]["Name"]
                    except KeyError:
                        self.logger.error("Data for language '" + actor_language + "' missing in Dene.ini" + "|" + participant["Short name"])
                        SubElement(actor_language_element, "Id").text = "Unknown"
                        SubElement(actor_language_element, "Name").text = actor_language

                    if actor_language in participant["First languages"]:
                        SubElement(actor_language_element, "MotherTongue").text = "true"
                    else:
                        SubElement(actor_language_element, "MotherTongue").text = "false"

                    if not participant["Main language"]:
                        SubElement(actor_language_element, "PrimaryLanguage").text = "Unspecified"
                    elif actor_language == participant["Main language"]:
                        SubElement(actor_language_element, "PrimaryLanguage").text = "true"
                    else:
                        SubElement(actor_language_element, "PrimaryLanguage").text = "false"

                # finally add the 'Actor' element under the right short name
                self.participants[participant["Short name"]] = actor_element


    def get_files(self):
        """Get all metadata of the resources from files.csv"""
        try:
            # open files.csv for reading
            files_file = open(self.args.files, "r")
        except FileNotFoundError:
            print("Couldn't find files.csv at", self.args.files)
            sys.exit(1)
        else:
            # first get the recording qualities which are needed when creating the 'MediaFile' elements
            quality = self.get_qualities()

            # go through each file
            for file in csv.DictReader(files_file):

                # first create 'ResourceProxy' elments of CMD/ResourceProxyList
                resource_proxy_element = Element("ResourceProxy", id=file["File name"])
                SubElement(resource_proxy_element, "ResourceType", mimetype=file["Format"]).text = self.config["CMD"]["ResourceType"]
                SubElement(resource_proxy_element, "ResourceRef").text = file["Location"]


                # then create 'MediaFile'/'WrittenResource' elements of CMD/Components/Session
                # check if it is a media file or a written resource
                file["Type"] = file["Type"].lower()
                is_media_file = file["Type"] == "video" or file["Type"] == "audio"
                if is_media_file:
                    resource_element = Element("MediaFile")

                    for key, value in [
                        ("ResourceLink", file["Location"]),
                        ("Type", file["Type"]),
                        ("Format", file["Format"]),
                        ("Size", file["Byte size"])
                        ]:

                        SubElement(resource_element, key).text = value

                    try:
                        SubElement(resource_element, "Quality").text = quality[file["Recording code"]]
                    except KeyError:
                        self.logger.error("Recording code '" + file["Recording code"] + "' missing in monitor.csv")
                        SubElement(resource_element, "Quality").text = "Unknown"

                    SubElement(resource_element, "RecordingConditions").text = "Unspecified"
                    time_position_element = SubElement(resource_element, "TimePosition")
                    SubElement(time_position_element, "Start").text = "00:00:00"
                    if file["Duration"]:
                        SubElement(time_position_element, "End").text = file["Duration"]

                else:
                    resource_element = Element("WrittenResource")

                    for key, value in [
                        ("ResourceLink", file["Location"]),
                        ("MediaResourceLink", ""),
                        ("Type", file["Type"]),
                        ("SubType", ""),
                        ("Format", file["Format"]),
                        ("Derivation", ""),
                        ("CharacterEncoding", "UTF-8"),
                        ("ContentEncoding", ""),
                        ("LanguageId", self.config["LanguageId"]["WrittenResource"]),
                        ("Anonymized", "false")
                        ]:

                        SubElement(resource_element, key).text = value

                    validation_element = SubElement(resource_element, "Validation")

                    for key, value in [("Type", ""), ("Methodology", ""), ("Level", "")]:
                        SubElement(validation_element, key).text = value


                access_element = SubElement(resource_element, "Access")
                for key, value in self.config.items("Access"):
                    SubElement(access_element, key).text = value
                contact_element = SubElement(access_element, "Contact")
                for key, value in self.config.items("Contact"):
                    SubElement(contact_element, key).text = value

                keys_element = SubElement(resource_element, "Keys")
                SubElement(keys_element, "Key", Name="RecordingCode").text = file["Recording code"]

                # finally add both resource elements under the right session code
                if is_media_file:
                    # prepend since media files must come before written resources
                    self.resources[file["Session code"]].insert(0, (resource_proxy_element, resource_element))
                else:
                    self.resources[file["Session code"]].append((resource_proxy_element, resource_element))


    def get_qualities(self):
        """Get for each recording its quality"""
        try:
            # open monitor.csv for reading
            monitor_file = open(self.args.monitor, "r")
        except FileNotFoundError:
            print("Couldn't find monitor.csv at", self.args.monitor)
            sys.exit(1)
        else:
            quality = {}
            quality_mapping = {"low": "1", "high": "5", "medium": "3", "": "Unspecified"}

            monitor_reader = csv.DictReader(monitor_file)

            # skip line with value 'quality' under 'quality of recording'

            for row in monitor_reader:
                try:
                    quality[row["recording name"]] = quality_mapping[row["quality"]]
                except KeyError:
                    self.logger.error("Unknown quality: " + row["quality"] + "|" + row["recording name"])
                    quality[row["recording name"]] = "Unknown"

            return quality


def main():
    """Generate all IMDI files for Dene"""
    imdi_maker = IMDIMaker()
    imdi_maker.generate_imdis()


if __name__ == '__main__':
    main()
