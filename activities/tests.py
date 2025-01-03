from django.test import TestCase
from .forms import SubmissionForm
from .models import Submission

class SubmissionFormTest(TestCase):
    def test_submission_form(self):
        with open('testfile.txt', 'w') as f:
            f.write('Sample Content')
        with open('testfile.txt', 'rb') as f:
            form_data = {'submitted_file': f}
            form = SubmissionForm(data=form_data, files={'submitted_file': f})
            self.assertTrue(form.is_valid())
