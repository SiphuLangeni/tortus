from tortus import tortus
from pathlib import Path
import pandas as pd
import pytest


@pytest.fixture(scope='session')
def load_sample_dfs():
    '''Fixture to load df and annotations'''
    csv_path = Path(__file__).resolve().parent / '..' / 'sample_project'
    reviews_path = csv_path / 'movie_reviews.csv'
    annotations_path = csv_path / 'movie_reviews_annotations.csv'
    reviews_df = pd.read_csv(reviews_path)
    annotations = pd.read_csv(annotations_path)
    return reviews_df, annotations

 
@pytest.fixture
def TortusRequired(load_sample_dfs):
    '''Instantiate Tortus with required parameters'''
    df = load_sample_dfs[0]
    tortus_instance = tortus.Tortus(df, 'reviews')
    return tortus_instance


def test_make_html(TortusRequired):
    '''Test if text string is placed between <h4></h4> tags'''
    # Setup
    text = 'This is only a test!'
    html = '<h4>This is only a test!</h4>'

    # Exercise
    result = TortusRequired.make_html(text)

    # Verify
    assert result == html


def test_create_subset_df(TortusRequired):
    '''Test creation of subset df when annotations=None'''
    assert TortusRequired.create_subset_df


@pytest.fixture(scope='class')
def TortusAnnotations(load_sample_dfs):
    '''Instantiate Tortus with optional parameter annotations'''
    df, annotations = load_sample_dfs
    tortus_instance = tortus.Tortus(df, 'reviews', annotations=annotations)
    return tortus_instance

def test_exclude_annotations_from_subset_df(TortusAnnotations):
    '''Ensure previous annotations not included in annotation widget'''
    # Setup 
    annotations_list = TortusAnnotations.annotations['reviews'].to_list()
    subset_df = TortusAnnotations.create_subset_df()
    subset_df_list = subset_df['reviews'].to_list()

    # Exercise
    result =  any(item in annotations_list for item in subset_df_list)

    # Verify
    assert result == False