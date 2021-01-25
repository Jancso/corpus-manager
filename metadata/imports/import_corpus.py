import configparser

from io import StringIO

from metadata.models import Corpus


def import_corpus(file):
    config = configparser.ConfigParser()
    config.read_file(StringIO(file))
    corpus = Corpus.objects.first()

    corpus.name = config['CMD']['MdCollectionDisplayName']
    corpus.link = config['CMD']['MdSelfLink']
    corpus.save()

    # set location
    corpus.location.continent = config['Location']['Continent']
    corpus.location.country = config['Location']['Country']
    corpus.location.region = config['Location']['Region']
    corpus.location.save()

    # set project
    corpus.project.name = config['Project']['Name']
    corpus.project.title = config['Project']['Title']
    corpus.project.pid = config['Project']['Id']
    corpus.project.description = config['Project']['descriptions']
    corpus.project.save()

    # set content
    corpus.content.genre = config['Content']['Genre']
    corpus.content.subgenre = config['Content']['SubGenre']
    corpus.content.task = config['Content']['Task']
    corpus.content.modalities = config['Content']['Modalities']
    corpus.content.subject = config['Content']['Subject']
    corpus.content.save()

    # set communication context
    corpus.content.communication_context.interactivity = config['CommunicationContext']['Interactivity']
    corpus.content.communication_context.planning_type = config['CommunicationContext']['PlanningType']
    corpus.content.communication_context.involvement = config['CommunicationContext']['Involvement']
    corpus.content.communication_context.social_context = config['CommunicationContext']['SocialContext']
    corpus.content.communication_context.event_structure = config['CommunicationContext']['EventStructure']
    corpus.content.communication_context.channel = config['CommunicationContext']['Channel']
    corpus.content.communication_context.save()

    # set contact
    corpus.project.contact.name = config['Contact']['Name']
    corpus.project.contact.address = config['Contact']['Address']
    corpus.project.contact.email = config['Contact']['Email']
    corpus.project.contact.organisation = config['Contact']['Organisation']
    corpus.project.contact.save()

    # set access
    corpus.access.availability = config['Access']['Availability']
    corpus.access.date = None
    corpus.access.owner = config['Access']['Owner']
    corpus.access.publisher = config['Access']['Publisher']
    corpus.access.save()

