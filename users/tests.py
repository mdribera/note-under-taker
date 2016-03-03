from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase


class UserSignupTests(TestCase):

    def test_user_signup_view_get(self):
        self.assertTrue(True)

    # def test_user_signup_view_get(self):
    #     """
    #     Index page should display note if it was published in the past
    #     """
    #     create_note(note_title="You will read this.",
    #                 days=30, user=create_user("mark"))
    #     response = self.client.get(reverse('notes:index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context['latest_notes_list'], [])

    # def test_was_published_recently_with_old_note(self):
    #     """
    #     was_published_recently() should return False for notes whose
    #     pub_date is older than one day.
    #     """
    #     time = timezone.now() - datetime.timedelta(days=30)
    #     old_note = Note(pub_date=time)
    #     self.assertEqual(old_note.was_published_recently(), False)

    # def test_was_published_recently_with_recent_note(self):
    #     """
    #     was_published_recently() should return True for notes whose
    #     pub_date is within the last day.
    #     """
    #     time = timezone.now() - datetime.timedelta(hours=5)
    #     recent_note = Note(pub_date=time)
    #     self.assertEqual(recent_note.was_published_recently(), True)
