from django.contrib import admin
from . import models


@admin.register(models.MeaningModel)
class MeaningModelAdmin(admin.ModelAdmin):
    list_display = ("word",)


@admin.register(models.SoundModel)
class SoundModelAdmin(admin.ModelAdmin):
    list_display = ("word",)


@admin.register(models.MyKanji)
class MyKanjiAdmin(admin.ModelAdmin):
    list_display = ("student", "kanji", "count", "is_clear", "is_right")


@admin.register(models.Kanji)
class KanjiAdmin(admin.ModelAdmin):
    list_display = (
        "shape",
        "alphabeticalOrderIndex",
        "newspaperFrequencyRank",
        "is_common_kanji",
        "is_meaningful",
    )

    # ManyToManyField는 어떻게 검색할 수 있는 지 구글링해야됨
    search_fields = ("alphabeticalOrderIndex",)

    filter_horizontal = ("meaning", "sound")
