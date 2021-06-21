Feature: Download Face Images From Flask
    In order to See if the pipeline can download face images 

Scenario: Fails To Download
    Given The PipeLine Tryed to download the images and failed
    When the website returns 404 error
    Then the pipeline should return an Execption


Scenario: Successfully Downloads
    Given The pipeline Tryed to download the images and passed
    When wget downloads the jpg
    Then should keep running the pipeline