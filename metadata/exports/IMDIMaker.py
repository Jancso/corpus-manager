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
import argparse
import datetime
import configparser
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Optional

from lxml.etree import *

from metadata.models import Participant, Recording, File, Corpus, Session, \
    Language


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

    def __init__(self, new_version=False, imdi_zip_dir_path=None):
        """Intialize variables for metadata files."""
        # get parsed arguments
        self.args = commandline_setup()

        self.new_version = new_version
        self.corpus = Corpus.objects.first()

        # some constants that were previously in Dene_IMDI.ini
        self.language_id_description = 'ISO639:eng'
        self.cmd_resource_type = 'Resource'
        self.language_id_written_resource = 'eng'

        # load Dene.ini where all the fixed values are stored
        self.config = configparser.ConfigParser()
        # preserve case
        self.config.optionxform = str
        if not self.config.read(self.args.ini):
            print("Couldn't find Dene_IMDI.ini at", self.args.ini)
            sys.exit(1)

        # intialize variables storing metadata
        self.session_metadata: Optional[Session] = None
        self.participants = {}
        self.resources = defaultdict(list)

        self.imdi_zip_path = Path(imdi_zip_dir_path)
        with zipfile.ZipFile(str(imdi_zip_dir_path), 'w') as archive:
            self.archive = archive
            # archive.write(video_dir / 'bboxes.json', 'bboxes.json')

        self.imdi_dir_path = Path(imdi_zip_dir_path)
        if not self.imdi_dir_path.exists():
            self.imdi_dir_path.mkdir()

    def generate_imdis(self):
        """Generate IMDI's for all sessions from session.csv"""
        # get and store metadata of all participants and files
        self.get_participants()
        self.get_files()

        for session in Session.objects.all():

            # store metadata of this session
            self.session_metadata = session

            # check in which IMDI version the file should be created
            if self.new_version:
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
        if self.new_version:
            session_element = Element("Session")
        else:
            session_element = SubElement(components_element, "Session")

        for key, value in [
                ("Name", self.session_metadata.name),
                ("Title", self.session_metadata.title),
                ("Date", self.session_metadata.date)
        ]:
            SubElement(session_element, key).text = value

        if self.session_metadata.situation:
            descriptions_element = SubElement(session_element, "descriptions")
            SubElement(
                descriptions_element,
                "Description",
                LanguageId=self.language_id_description).text = self.session_metadata.situation

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

    def create_mdgroup(self, session_element):
        """Create IMDI element 'MDGroup'"""
        mdgroup_element = SubElement(session_element, "MDGroup")
        self.create_location(mdgroup_element)
        self.create_project(mdgroup_element)

        keys_element = SubElement(mdgroup_element, "Keys")
        SubElement(
            keys_element,
            "Key",
            Name="Duration").text = self.session_metadata.duration

        self.create_content(mdgroup_element)
        self.create_actors(mdgroup_element)

    def create_location(self, mdgroup_element):
        """Create IMDI element 'Location'"""
        location_element = SubElement(mdgroup_element, "Location")

        for key, value in [
                ("Continent", self.corpus.location.continent),
                ("Country", self.corpus.location.country),
                ("Region", self.corpus.location.region)
        ]:
            SubElement(location_element, key).text = value

        SubElement(
            location_element,
            "Address").text = self.session_metadata.location

    def create_project(self, mdgroup_element):
        """Create IMDI element 'Project'"""
        project_element = SubElement(mdgroup_element, "Project")

        for key, value in [
                ("Name", self.corpus.project.name),
                ("Title", self.corpus.project.title),
                ("Id", self.corpus.project.pid)
        ]:
            SubElement(project_element, key).text = value

        contact_element = SubElement(project_element, "Contact")
        for key, value in [
                ('Name', self.corpus.project.contact.name),
                ('Address', self.corpus.project.contact.address),
                ('Email', self.corpus.project.contact.email),
                ('Organisation', self.corpus.project.contact.organisation)
        ]:
            SubElement(contact_element, key).text = value

        descriptions_element = SubElement(project_element, "descriptions")
        SubElement(
            descriptions_element,
            "Description",
            LanguageId=self.language_id_description).text = self.corpus.project.description

    def create_content(self, mdgroup_element):
        """Create IMDI element 'Content'"""
        content_element = SubElement(mdgroup_element, "Content")

        for key, value in [
                ('Genre', self.corpus.content.genre),
                ('SubGenre', self.corpus.content.subgenre),
                ('Task', self.corpus.content.task),
                ('Modalities', self.corpus.content.modalities),
                ('Subject', self.corpus.content.subject)
        ]:
            SubElement(content_element, key).text = value

        context_element = SubElement(content_element, "CommunicationContext")

        context = self.corpus.content.communication_context

        for key, value in [
                ('Interactivity', context.interactivity),
                ('PlanningType', context.planning_type),
                ('Involvement', context.involvement),
                ('SocialContext', context.social_context),
                ('EventStructure', context.event_structure),
                ('Channel', context.channel)
        ]:
            SubElement(context_element, key).text = value

        content_languages_element = SubElement(content_element,
                                               "Content_Languages")

        for lang in Language.objects.all():
            content_language_element = SubElement(content_languages_element,
                                                  "Content_Language")
            for key, value in [
                ('Id', lang.iso_code),
                ('Name', lang.name),
                ('Dominant', 'Unspecified'),
                ('SourceLanguage', 'Unspecified'),
                ('TargetLanguage', 'Unspecified')
            ]:
                SubElement(content_language_element, key).text = value

        SubElement(content_element, "Keys")

        if self.session_metadata.content:
            descriptions_element = SubElement(content_element, "descriptions")
            SubElement(
                descriptions_element,
                "Description",
                LanguageId=self.language_id_description).text = self.session_metadata.content

    def create_actors(self, mdgroup_element):
        """Create IMDI element 'Actors'"""
        actors_element = SubElement(mdgroup_element, "Actors")

        for actor in self.session_metadata.sessionparticipant_set:

            # get the right actor element
            actor_element = self.participants[actor.participant.short_name]

            # role (select the first one)
            role = actor.roles.first().name

            # modify the fields whose values depend on the role of an actor
            if role == "researcher":
                # change 'Role' element
                actor_element[0].text = role
                # change 'FamilySocialRole' element
                actor_element[4].text = "Not-related"
            elif role == "recorder":
                actor_element[0].text = role
                actor_element[4].text = "Not-related"
            else:
                actor_element[0].text = "Speaker"
                actor_element[4].text = role

            # age of actor at this session
            if actor.age:
                actor_element[6].text = str(actor.age)
            else:
                actor_element[6].text = 'Unspecified'

            # finally add the actor element
            actors_element.append(actor_element)

    def create_session_resources(self, session_element):
        """Create IMDI element 'Resources'"""
        resources_element = SubElement(session_element, "Resources")

        for resource_proxy_element, resource_element in self.resources[self.session_metadata["Code"]]:
            resources_element.append(resource_element)

    def get_participants(self):
        """Get all metadata of the partcipants."""
        participants = Participant.objects.all()
        # go through each participant
        for participant in participants:

            actor_element = Element("Actor")

            for key, value in [
                ("Role", ""),
                ("Name", participant.full_name.split(" ")[0]),
                ("FullName", participant.full_name),
                ("Code", participant.short_name),
                ("FamilySocialRole", ""),
                ("EthnicGroup", participant.ethnic_group),
                ("Age", ""),
                ("BirthDate", participant.get_birth_date()),
                ("Sex", participant.gender),
                ("Education", participant.education),
                ("Anonymized", "false")
                ]:

                if value:
                    SubElement(actor_element, key).text = value
                else:
                    SubElement(actor_element, key).text = "Unspecified"

            SubElement(actor_element, "Keys")

            if participant.description:
                descriptions_element = SubElement(actor_element, "descriptions")
                SubElement(
                    descriptions_element,
                    "Description",
                    LanguageId=self.language_id_description).text = participant.description

            actor_languages_element = SubElement(actor_element, "Actor_Languages")

            if participant.language_biography:
                descriptions_element = SubElement(actor_languages_element, "descriptions")
                SubElement(descriptions_element,
                           "Description",
                           LanguageId=self.language_id_description).text = participant.language_biography

            # then create an 'Actor_Language' element for each language
            # spoken by this actor
            for actor_language in participant.participantlanginfo_set:
                actor_language_element = SubElement(actor_languages_element, "Actor_Language")

                SubElement(actor_language_element, "Id").text = actor_language.language.iso_code
                SubElement(actor_language_element, "Name").text = actor_language.language.name

                if actor_language.first:
                    SubElement(actor_language_element, "MotherTongue").text = "true"
                else:
                    SubElement(actor_language_element, "MotherTongue").text = "false"

                if actor_language.main is None:
                    SubElement(actor_language_element, "PrimaryLanguage").text = "Unspecified"
                elif actor_language.main:
                    SubElement(actor_language_element, "PrimaryLanguage").text = "true"
                else:
                    SubElement(actor_language_element, "PrimaryLanguage").text = "false"

            # finally add the 'Actor' element under the right short name
            self.participants[participant.short_name] = actor_element

    def get_files(self):
        """Get all metadata of the resources from files.csv"""
        # first get the recording qualities
        # which are needed when creating the 'MediaFile' elements
        quality = self.get_qualities()

        for file in File.objects.all():

            # first create 'ResourceProxy' elments of CMD/ResourceProxyList
            resource_proxy_element = Element("ResourceProxy", id=file.name)
            SubElement(
                resource_proxy_element,
                "ResourceType",
                mimetype=file.get_mime_type()).text = self.cmd_resource_type
            SubElement(
                resource_proxy_element,
                "ResourceRef").text = file.location

            # then create 'MediaFile'/'WrittenResource' elements
            # of CMD/Components/Session
            # check if it is a media file or a written resource
            is_media_file = file.type in [File.TYPE_VIDEO, File.TYPE_AUDIO]
            if is_media_file:
                resource_element = Element("MediaFile")

                for key, value in [
                        ("ResourceLink", file.location),
                        ("Type", file.type),
                        ("Format", file.get_mime_type()),
                        ("Size", file.size)
                ]:
                    SubElement(resource_element, key).text = value

                SubElement(
                    resource_element,
                    "Quality").text = quality[file.recording.name]

                SubElement(
                    resource_element,
                    "RecordingConditions").text = "Unspecified"
                time_position_element = SubElement(resource_element,
                                                   "TimePosition")
                SubElement(time_position_element, "Start").text = "00:00:00"
                if file.duration:
                    SubElement(
                        time_position_element,
                        "End").text = file.duration
            else:
                resource_element = Element("WrittenResource")

                for key, value in [
                        ("ResourceLink", file.location),
                        ("MediaResourceLink", ""),
                        ("Type", file.type),
                        ("SubType", ""),
                        ("Format", file.get_mime_type()),
                        ("Derivation", ""),
                        ("CharacterEncoding", "UTF-8"),
                        ("ContentEncoding", ""),
                        ("LanguageId", self.language_id_written_resource),
                        ("Anonymized", "false")
                ]:
                    SubElement(resource_element, key).text = value

                validation_element = SubElement(resource_element, "Validation")

                for key, value in [("Type", ""),
                                   ("Methodology", ""),
                                   ("Level", "")]:
                    SubElement(validation_element, key).text = value

            access_element = SubElement(resource_element, "Access")
            for key, value in [
                    ('Availability', self.corpus.access.availability),
                    ('Date', self.corpus.access.date),
                    ('Owner', self.corpus.access.date),
                    ('Publisher', self.corpus.access.publisher)
            ]:
                SubElement(access_element, key).text = value
            contact_element = SubElement(access_element, "Contact")
            for key, value in [
                    ('Name', self.corpus.project.contact.name),
                    ('Address', self.corpus.project.contact.address),
                    ('Email', self.corpus.project.contact.email),
                    ('Organisation', self.corpus.project.contact.organisation)
            ]:
                SubElement(contact_element, key).text = value

            keys_element = SubElement(resource_element, "Keys")
            SubElement(
                keys_element,
                "Key",
                Name="RecordingCode").text = file.recording.name

            # finally add both resource elements under the right session code
            if is_media_file:
                # prepend since media files must come before written resources
                self.resources[file.recording.session.name].insert(
                    0, (resource_proxy_element, resource_element))
            else:
                self.resources[file.recording.session.name].append(
                    (resource_proxy_element, resource_element))

    def get_qualities(self):
        """Get for each recording its quality"""
        quality = {}
        quality_mapping = {
            "low": "1",
            "high": "5",
            "medium": "3",
            "n/a": "Unspecified"
        }

        for rec in Recording.objects.all():
            quality[rec.name] = quality_mapping[rec.get_quality_display()]

        return quality


def main():
    """Generate all IMDI files for Dene"""
    imdi_maker = IMDIMaker()
    imdi_maker.generate_imdis()


if __name__ == '__main__':
    main()
