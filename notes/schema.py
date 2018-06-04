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
        #import pdb; pdb.set_trace()

        if title is not None:
            return Note.objects.get(title=title)

        return None

class CreateNote(graphene.Mutation):
    class Arguments:
        # Input attributes for the mutation
        title = graphene.String()
        content = graphene.String()

    ok = graphene.Boolean()
    note = graphene.Field(NoteType)

    def mutate(self, info, title, content):
        new_user = info.context.user

        if new_user.is_anonymous:
            new_ok = False
            return CreateNote(ok=new_ok)
        else:
            new_note = Note(title=title, content=content, user=new_user)
            new_ok = True
            new_note.save()
            return CreateNote(note=new_note, ok=new_ok)

class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()



# Add a schema and attach the query
schema = graphene.Schema(query=Query, mutation=Mutation)
