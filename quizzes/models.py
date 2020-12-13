import random
from django.db import models
from kanji.models import Kanji, MyKanji

# 객관식 보기를 만드는 게 나을 듯


class Question(models.Model):
    quiz = models.ForeignKey("Quiz", related_name="questions", on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    kanji_answer = models.ForeignKey(
        "kanji.Kanji", related_name="kanji_questions", on_delete=models.CASCADE
    )
    word_answer = models.ForeignKey(
        "kanji.Kanji", related_name="word_questions", on_delete=models.CASCADE
    )
    submitted_meaning = models.CharField(max_length=15, blank=True)
    submitted_sound = models.CharField(max_length=15, blank=True)
    submitted_number = models.IntegerField(default=-1, blank=True)
    is_right = models.BooleanField(default=None, null=True)
    is_clear = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quiz} - {self.index}"

    def score_kr_quiz(self, submitted):
        meaning_right = True
        sound_right = True
        self.submitted_meaning = submitted["meaning"]
        self.submitted_sound = submitted["sound"]
        self.is_clear = submitted["clarity"]
        meaning_answer = self.answer.meaning.replace(" ", "").split("/")
        sound_answer = self.answer.sound.replace(" ", "").split("/")
        if self.submitted_meaning not in meaning_answer:
            meaning_right = False
        if self.submitted_sound not in sound_answer:
            sound_right = False
        is_right = meaning_right and sound_right
        self.is_right = is_right
        self.save()

    class Meta:
        ordering = ["quiz", "index"]


class Quiz(models.Model):

    TYPE_MULTIPLE = "multiple"
    TYPE_SHORT_JP = "short_jp"
    TYPE_SHORT_KR = "short_kr"

    TYPE_CHOICES = (
        (TYPE_MULTIPLE, "객관식"),
        (TYPE_SHORT_JP, "한자 맞추기"),
        (TYPE_SHORT_KR, "한국 음훈 맞추기"),
    )

    limit = models.IntegerField()
    start = models.IntegerField(default=1)
    end = models.IntegerField(default=2136)
    student = models.ForeignKey(
        "users.User", related_name="quizzes", on_delete=models.CASCADE
    )
    exam = models.ForeignKey("Exam", related_name="quizzes", on_delete=models.CASCADE)
    quiz_type = models.CharField(choices=TYPE_CHOICES, max_length=20)

    def __str__(self):
        return f"{self.student.username} - {self.created_at}"

    def number_of_questions(self):
        return self.questions.count()

    def delete(self, *args, **kwargs):
        query = models.Q(is_clear=False) | models.Q(is_right=False)
        questions = self.questions.filter(query)
        for question in questions:
            try:
                my_kanji = MyKanji.objects.get(
                    student=self.student, kanji=question.answer
                )
                if not question.is_right:
                    my_kanji.is_right = False
                    my_kanji.count += 1
                if not question.is_clear:
                    my_kanji.is_clear = False
                my_kanji.save()
            except MyKanji.DoesNotExist:
                if question.is_right:
                    MyKanji.objects.create(
                        student=self.student,
                        kanji=question.answer,
                        is_right=True,
                        is_clear=False,
                    )
                else:
                    MyKanji.objects.create(
                        student=self.student,
                        kanji=question.answer,
                        count=1,
                        is_clear=question.is_clear,
                    )
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        kanji = list(Kanji.objects.filter(index__range=(self.start, self.end)))
        random.shuffle(kanji)
        limit = self.limit if self.limit <= self.end + 1 else self.end + 1
        kanji = kanji[:limit]
        index = 0
        if self.quiz_type != self.TYPE_MULTIPLE:
            for char in kanji:
                Question.objects.create(
                    quiz=self, question_type=self.quiz_type, answer=char, index=index
                )
                index += 1

    class Meta:
        verbose_name_plural = "Quizzes"


class Exam(models.Model):

    TYPE_RANDOM = "random"
    TYPE_MULTIPLE = "multiple"
    TYPE_SHORT_JP = "short_jp"
    TYPE_SHORT_KR = "short_kr"

    TYPE_CHOICES = (
        (TYPE_MULTIPLE, "객관식"),
        (TYPE_RANDOM, "모든 유형"),
        (TYPE_SHORT_JP, "한자 맞추기"),
        (TYPE_SHORT_KR, "한국 음훈 맞추기"),
    )

    student = models.ForeignKey(
        "users.User", related_name="exams", on_delete=models.CASCADE
    )
    exam_type = models.CharField(choices=TYPE_CHOICES, max_length=20)
    rest_kanji = models.ManyToManyField("kanji.Kanji", blank=True, symmetrical=False)

    def length_of_rest_kanji(self):
        return self.rest_kanji.count()
