from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    pass


class Field(models.Model):
    name = models.CharField(max_length=20, help_text="A name for this field of knowledge")
    super_field = models.ForeignKey("self", related_name="sub_fields", blank=True,
                                    help_text="The broader field that this field of knowledge resides in",
                                    on_delete=models.CASCADE)
    pre_req_fields = models.ManyToManyField("self", related_name="enabling_fields", blank=True, symmetrical=False,
                                            help_text="Fields that are important to learn before tackling this field "
                                                      "of knowledge")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fields_created")

    def number_of_subfields(self):
        return self.sub_fields.all().count()

    def nature_of_field(self):
        return "elemental" if self.number_of_subfields() == 0 else "collection"

    def number_of_pre_req_fields(self):
        return self.pre_req_fields.all().count()

    def number_of_enabling_fields(self):
        return self.enabling_fields.all().count()

    def __str__(self):
        name_of_field = f'"{self.name}", '
        nature_of_field = "an elemental field" if self.nature_of_field() == "elemental" else "a collection field. "
        requiring_fields = f"Requires: {', '.join([field.name for field in self.pre_req_fields.all()])}. " \
            if self.number_of_pre_req_fields() > 0 else ""
        satisfying_fields = f"Satisfies: {', '.join([field.name for field in self.enabling_fields.all()])}. " \
            if self.number_of_enabling_fields() > 0 else ""

        return name_of_field + nature_of_field + requiring_fields + satisfying_fields


class Mastery(models.Model):
    title = models.CharField(max_length=20, help_text="A name for this learning resource")
    link = models.URLField(blank=True, help_text="A URL to help access this learning resource, if any")
    description = models.TextField(help_text="A helpful description describing this learning resource")
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mastery_entries")

    def __str__(self):
        title = f'"{self.title}", '
        contributor = f"by {self.contributor}."
        return title + contributor


class Conversation(models.Model):
    class ConversationTypes(models.TextChoices):
        PAPER = 'paper', _('Academic Paper')
        EVENT = 'event', _('Historic Event')

    variety = models.CharField(
        max_length=5,
        choices=ConversationTypes.choices, help_text="What kind of a message is this?"
    )

    year = models.IntegerField(help_text="The year in which the event/paper occurred or was published")
    title = models.CharField(max_length=20, help_text="Name of event/paper")
    description = models.TextField(help_text="A helpful description for the event/paper. "
                                             "Personal takes are encouraged.")
    reference = models.CharField(max_length=2048, help_text="A reference to the event/paper, such as a URL")
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversation_entries")

    def __str__(self):
        year = f"{self.year}: "
        title = f'"{self.title}", '
        variety = "an event." if self.variety == "event" else "a paper."
        return year + title + variety
