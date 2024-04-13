from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import connection, reset_queries
from django.db.models.fields.json import KT
from django.test import TestCase, override_settings

from .models import Document, StringDocument


class StringDocumentTestCase(TestCase):
    def setUp(self):
        StringDocument.objects.create(
            title="String Document",
            body="""Example body with some text
across multiple lines.
""",
        )

        StringDocument.objects.create(
            title="String 2",
            body="does not have the word",
        )

        StringDocument.objects.create(
            title="String 3",
            body="is the EXAMPLING of examples for the example",
        )

    def test_search(self):
        results = StringDocument.objects.filter(body__search="The")
        # print(results.query)
        # SELECT "string_document"."id", "string_document"."title", "string_document"."author", "string_document"."body" FROM "string_document" WHERE to_tsvector(COALESCE("string_document"."body", '')) @@ (plainto_tsquery(Example))
        for item in results:
            print(item)

    def test_vector(self):
        # Print all vectors
        results = StringDocument.objects.annotate(
            vector=SearchVector("body", config="simple")
        )
        # print(results.query)
        # SELECT "string_document"."id",
        #        "string_document"."title",
        #        "string_document"."author",
        #        "string_document"."body"
        # FROM "string_document"
        # WHERE to_tsvector(COALESCE("string_document"."body", '')) @@ (plainto_tsquery('Example'));
        for item in results:
            print(item, item.vector)

    def test_complex(self):
        title_vector = SearchVector("title", config="French", weight="A")
        body_vector = SearchVector("body", config="French", weight="B")
        query = SearchQuery("Exemple")
        results = (
            StringDocument.objects.annotate(
                rank=SearchRank(title_vector + body_vector, query)
            )
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

        print("COMPLEX RESULTS:")
        for item in results:
            print(item, item.rank)


class FullTextSearchTestCase(TestCase):
    def setUp(self):
        Document.objects.create(
            content={
                "title": "Example Title",
                "author": "Myself",
                "body": "The body of example text that we would want to search.",
            }
        )
        Document.objects.create(
            content={
                "title": "File 2",
                "author": "Example of Myself",
                "body": "More text",
            }
        )

        Document.objects.create(
            content={
                "title": "French",
                "body": "Ceci est un exemple de texte français",
            }
        )

    def test_author(self):
        results = Document.objects.filter(content__author="Myself")
        print(results)

    def test_search(self):
        # reset_queries()
        results = Document.objects.filter(content__body__search="Example")
        # print(results.query)
        print(results)  # Make sure to evaluate the results
        # No results - tries to find a text match in the "search" property of content
        # SELECT "document"."id", "document"."content" FROM "document" WHERE ("document"."content" -> search) = '"More"'

    def test_french(self):
        vector = SearchVector("title", weight="A", config="french") + SearchVector(
            "body", weight="B", config="french"
        )
        query = SearchQuery("Exemple", config="french")

        results = (
            Document.objects.annotate(
                title=KT("content__title"),
                body=KT("content__body"),
                vector=vector,
                rank=SearchRank(vector, query),
            )
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

        for result in results:
            print(result, result.vector)

    def test_kt(self):
        # reset_queries()

        # results = Document.objects.annotate(body=KT("content__body")).filter(
        #     body__search="Example"
        # )
        # print(results.query)
        # print("KT:", results)  # Make sure to evaluate the results
        # No results - tries to find a text match in the "search" property of content
        # SELECT "document"."id", "document"."content" FROM "document" WHERE ("document"."content" -> search) = '"More"'

        vector = SearchVector("title", weight="A") + SearchVector("body", weight="B")
        query = SearchQuery("Example")

        results = (
            Document.objects.annotate(
                title=KT("content__title"),
                body=KT("content__body"),
                rank=SearchRank(vector, query),
            )
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

        for result in results:
            print(result)

    def test_vector(self):
        reset_queries()

        title_vector = SearchVector("content__title", weight="A")
        body_vector = SearchVector("content__body", weight="B")
        query = SearchQuery("Example")
        results = (
            Document.objects.annotate(
                rank=SearchRank(title_vector + body_vector, query)
            )
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )

        for result in results:
            print(result)

    #     # Use a search vector
    #     results = Document.objects.annotate(search=SearchVector("content__body")).
    #     # SELECT "document"."id", "document"."content", to_tsvector(COALESCE(("document"."content")::text, '')) AS "search" FROM "document" WHERE to_tsvector(COALESCE(("document"."content")::text, '')) @@ (plainto_tsquery(More))
    #     print([item for item in results])

    #     reset_queries()

    #     results = Document.objects.annotate(
    #         search=SearchVector("content__body")
    #     ).filter(search="More")

    #     # SELECT "document"."id", "document"."content", to_tsvector(COALESCE((("document"."content" -> 'body'))::text, '')) AS "search" FROM "document" WHERE to_tsvector(COALESCE((("document"."content" -> 'body'))::text, '')) @@ (plainto_tsquery(More))

    #     print(results.query)
    #     print([item for item in results])

    #     # Print all vectors
    #     for item in Document.objects.annotate(vector=SearchVector("content__body")):
    #         print(item, item.vector)

    #     # File 1 'block':7 'bodi':2 'exampl':1 'n':10 'na':6 'text':5,9
    #     # File 2 'text':2

    #     # Add weights
    #     # vector = SearchVector("content__title", weight="A") + SearchVector(
    #     #     "content__body", weight="B"
    #     # )

    # # def test_kt(self):

    # #     Document.objects.annotate(
    # #         header_text=KT("content__header"),
    # #         body_text=KT("content__body"),
    # #     )
    # #     .annotate(
    # #         rank=SearchRank(vector, SearchQuery(search)),
    # #     )
    # #     .filter(rank__gte=0.01)
