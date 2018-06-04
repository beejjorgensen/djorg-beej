from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import Note

#from graphene_django.filter import DjangoFilterConnectionField

class NoteType(DjangoObjectType):
    class Meta:
        model = Note

        # Describe the data as a node in the graph for GraphQL
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    note = graphene.Field(NoteType, id=graphene.Int(), title=graphene.String())
    all_notes = graphene.List(NoteType)

    def resolve_all_notes(self, info, **kwargs):
        return Note.objects.all()

    def resolve_note(self, info, **kwargs):
        title = kwargs.get('title')

        if title is not None:
            return Note.objects.get(title=title)

        return None


# Add a schema and attach the query
schema = graphene.Schema(query=Query)
