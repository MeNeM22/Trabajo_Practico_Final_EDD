"""
Tests para el módulo de web scraping.
"""

import pytest
import os
import src.scraping.tenTimesScrap as scrape10Times
import src.scraping.eventsEyeScrap as eventsEye
import src.scraping.nferiasScrap as nferias
#import src.scraping.10timesScrap as times

def test_eventseye_scraping():
    eventsEye.scrape_events_eye(1,5)

    assert os.path.exists("data/eventos.csv")

def test_eventseye_scrapingIsNone():
    result = eventsEye.scrape_events_eye(0,0)

    assert result is None

def test_nferias_scraping():
    nferias.scrap_nferias(1,1,5)
    
    assert os.path.exists("data/eventos.csv")

def test_nferias_scrapingIsNone():
    result = nferias.scrap_nferias(0,0,0)

    assert result is None

def test_10times_scraping():
    scrape10Times.scrape10Times()

    assert os.path.exists("data/eventos.csv")
   

def test_10times_scrapingIsNone():
    result = scrape10Times.scrape10Times(0,0) 

    assert result is None

def test_consolidate_events():

    with open ("data/eventos.csv", encoding="utf-8") as f:
        resultado = f.read()
    
    assert "nferias" in resultado
    assert "eventseye" in resultado
    assert "10times" in resultado

def test_handle_missing_data():

    with open ("data/eventos.csv", encoding="utf-8") as f:
        resultado = f.read()
    
    assert "No info" in resultado
