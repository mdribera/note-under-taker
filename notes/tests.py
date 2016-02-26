import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Note, Label

class NoteMethodTests(TestCase):
  def test_was_published_recently_with_future_note(self):
    """
    was_published_recently() should return False for notes whose
    pub_date is in the future.
    """
    time = timezone.now() + datetime.timedelta(days=30)
    future_note = Note(pub_date=time)
    self.assertEqual(future_note.was_published_recently(), False)

  def test_was_published_recently_with_old_note(self):
    """
    was_published_recently() should return False for notes whose
    pub_date is older than one day.
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_note = Note(pub_date=time)
    self.assertEqual(old_note.was_published_recently(), False)

  def test_was_published_recently_with_recent_note(self):
    """
    was_published_recently() should return True for notes whose
    pub_date is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=5)
    recent_note = Note(pub_date=time)
    self.assertEqual(recent_note.was_published_recently(), True)

class NoteIndexViewTests(TestCase):
  def test_index_view_with_no_notes(self):
    """
    If no notes exist, an appropriate message should be displayed.
    """
    response = self.client.get(reverse('notes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No notes are available.")
    self.assertQuerysetEqual(response.context['latest_notes_list'], [])

  def test_index_view_with_future_note(self):
    """
    Index page should display note if it was published in the past
    """
    create_note(note_title="You will read this.", days=30)
    response = self.client.get(reverse('notes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['latest_notes_list'], [])

  def test_index_view_with_past_note(self):
    """
    Index page should display note if it was published in the past
    """
    create_note(note_title="Something about the past.", days=-30)
    response = self.client.get(reverse('notes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(
    response.context['latest_notes_list'],
      ['<Note: Something about the past.>']
    )

  def test_index_view_with_past_and_future_notes(self):
    """
    Index page should display note if it was published in the past
    """
    create_note(note_title="Something about the past.", days=-30)
    create_note(note_title="A future note.", days=30)
    response = self.client.get(reverse('notes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(
    response.context['latest_notes_list'],
      ['<Note: Something about the past.>']
    )

  def test_index_view_with_two_past_notes(self):
    """
    Index page should display note if it was published in the past
    """
    create_note(note_title="Thing 1", days=-2)
    create_note(note_title="Thing 2", days=-3)
    response = self.client.get(reverse('notes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(
    response.context['latest_notes_list'],
      ['<Note: Thing 1>', '<Note: Thing 2>']
    )

class NoteIndexViewWithLabelTests(TestCase):
  def test_label_view_not_found(self):
    """
    If given label doesn't exist return a 404
    """
    response = self.client.get('/notes/?label=notalabel')
    self.assertEqual(response.status_code, 404)

  def test_label_view_no_notes_found(self):
    """
    If there aren't any notes associated with a certain label
    an appropriate message should be displayed.
    """
    new_label = create_label("Journal")
    response = self.client.get('/notes/?label=' + new_label.text)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No notes are available.")
    self.assertQuerysetEqual(response.context['latest_notes_list'], [])

  def test_label_view_past_notes_found(self):
    """
    The list view of notes associated with a given label
    """
    new_label = create_label(label_text="Journal")
    past_note_one = create_note_with_label(note_title="Dear diary", days=-5, label=new_label.id)
    past_note_two = create_note_with_label(note_title="February 24th, 2016", days=-4, label=new_label.id)
    response = self.client.get('/notes/?label=' + new_label.text)
    self.assertContains(response, past_note_one.note_title, status_code=200)
    self.assertContains(response, past_note_two.note_title, status_code=200)
    self.assertQuerysetEqual(response.context['latest_notes_list'], ['<Note: February 24th, 2016>', '<Note: Dear diary>'])

class NoteDetailViewTests(TestCase):
  def test_detail_view_not_found(self):
    """
    The detail view of a note whose pub_date is in the future
    should return a 404
    """
    future_note = create_note(note_title="You're in the future, man!", days=30)
    response = self.client.get(reverse('notes:detail', args=(future_note.id,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_view_with_past_note(self):
    """
    The detail view of a note whose pub_date is in the past
    should display its title and text
    """
    past_note = create_note(note_title="Hogwarts, a history", days=-5)
    response = self.client.get(reverse('notes:detail', args=(past_note.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, past_note.note_title, status_code=200)

def create_note(note_title, days):
  """
  Creates a Note with the given `note_title` and published the
  given number of `days` offset to now (negative for notes published
  in the past, positive for notes that have yet to be published).
  """
  time = timezone.now() + datetime.timedelta(days=days)
  return Note.objects.create(note_title=note_title, pub_date=time)

def create_note_with_label(note_title, days, label):
  """
  Creates a Note with the given `note_title`, associated with given `label`,
  and published the given number of `days` offset to now (negative for notes
  published in the past, positive for notes that have yet to be published).
  """
  time = timezone.now() + datetime.timedelta(days=days)
  note = Note.objects.create(note_title=note_title, pub_date=time)
  note.labels.add(label)
  return note

def create_label(label_text):
  """ Creates a Label with the given `text` """
  return Label.objects.create(text=label_text)
