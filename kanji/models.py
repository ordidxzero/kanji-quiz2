from typing import Text
from django.db import models


class TextModel(models.Model):
    word = models.CharField(max_length=30)


class MeaningModel(TextModel):
    pass


class SoundModel(TextModel):
    pass


class MyKanji(models.Model):
    student = models.ForeignKey(
        "users.User", related_name="my_kanji", on_delete=models.CASCADE
    )
    kanji = models.ForeignKey("Kanji", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    is_right = models.BooleanField(default=False)
    is_clear = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.kanji}"


class Kanji(models.Model):
    shape = models.CharField(max_length=10)
    meaning = models.ManyToManyField(MeaningModel, related_name="kanji", blank=True)
    sound = models.ManyToManyField(SoundModel, related_name="kanji", blank=True)
    alphabeticalOrderIndex = models.IntegerField(default=99999)
    newspaperFrequencyRank = models.IntegerField(default=99999)
    strokeOrderGifUri = models.CharField(max_length=200, blank=True)
    is_meaningful = models.BooleanField(default=True)
    is_common_kanji = models.BooleanField(default=True)

    def __str__(self):
        return self.shape

    class Meta:
        ordering = ["alphabeticalOrderIndex"]
