# -*- coding: UTF-8 -*-

try:
    from django.db import models
    from django.utils.safestring import mark_for_escaping as _escape

    from interlinears import make_html_interlinear

    class InterlinearModel(models.Model):
        """Mixin for Django models to give them an interlinear field with
        the necessary logic."""

        INTERLINEAR_FORMATS = (
                ('monospace', 'WYSIWYG monospace'),
                ('leipzig', 'Leipzig Glossing Rules'),
        )

        interlinear = models.TextField('Interlinear', blank=True, default='', db_column='il_text')
        il_xhtml = models.TextField('Interlinear, formatted', blank=True, default='', db_column='il_xhtml')
        il_format = models.CharField('Interlinear format', max_length=20, choices=INTERLINEAR_FORMATS, blank=True, default='monospace')

        class Meta:
            abstract = True

        def get_interlinear(self):
            return make_html_interlinear(self.interlinear, self.il_format, _escape)

        def save(self, *args, **kwargs):
            new_il = self.get_interlinear()
            if new_il:
                self.il_xhtml = new_il
            super(Interlinear, self).save(*args, **kwargs)

except ImportError:
    # Django not in path, do nothing
    pass
