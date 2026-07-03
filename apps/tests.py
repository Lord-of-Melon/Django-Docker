from django.test import TestCase
from django.db import connection
from apps.models import Course

class QueryTest(TestCase):
    def test_listing_queries(self):
        list(Course.objects.for_listing())
        self.assertTrue(len(connection.queries) >= 1)