from music_generation.data.genre_metadata_extractor import GenreMetadataExtractor



def test_rock_genre():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["rock","punk","alternative rock"])
    assert genres == ["rock"]
    assert scores["rock"] >= 3


def test_pop_genre():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["dance pop","teen pop","europop"])
    assert genres == ["pop"]
    assert scores["pop"] >= 3


def test_jazz_genre():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["jazz","bebop","latin jazz"])
    assert genres == ["jazz"]
    assert scores["jazz"] >= 3


def test_classical_genre():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["baroque","concerto","orchestral"])
    assert genres == ["classical"]
    assert scores["classical"] >= 3


def test_multi_label_genre():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["classic pop and rock"])
    assert set(genres) == {"pop","rock"}
    assert scores["pop"] == 1
    assert scores["rock"] == 1


def test_no_matching_genre():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["techno","house","trance"])
    assert genres == []
    assert scores["classical"] == 0
    assert scores["jazz"] == 0
    assert scores["pop"] == 0
    assert scores["rock"] == 0


def test_case_insensitive_tags():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["CLASSIC ROCK","PuNk"])
    assert genres == ["rock"]
    assert scores["rock"] >= 2


def test_musicbrainz_style_tag():
    extractor = GenreMetadataExtractor()
    genres, scores = extractor.assign_genre(["rock and indie"])
    assert genres == ["rock"]
    assert scores["rock"] >= 1


def test_pop_rock_tie():
    extractor = GenreMetadataExtractor()
    genres, _ = extractor.assign_genre(
        ["classic pop and rock"]
    )
    assert set(genres) == {"pop","rock",}