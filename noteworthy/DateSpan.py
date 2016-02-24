class DateSpan(models.Model):
  content_type = models.ForeignKey(ContentType, related_name='datespans')
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')

  start_date = models.DateField()
  end_date = models.DateField(null=True)

  def __str__(self):
    return self.fancy_string

  @property
  def fancy_string(self):
    start = datetime.strptime(self.start_date, '%Y-%m-%d')
    start_string = start.strftime('%B %Y')

      end_string = 'Present'
      if self.end_date:
        end = datetime.strptime(self.end_date, '%Y-%m-%d')
        end_string = end.strftime('%B %Y')

      return '%s - %s' % (start_string, end_string)