# Plague Doc's Search Engine

## About the Project

<p>The Plague Doc's Search Engine is a relevance ranked search engine that uses `The Cornell Movie-Dialogue Corpus` as data. `(source: https://www.kaggle.com/Cornell-University/movie-dialog-corpus)`
It allows the user to search for words that appear in movie scripts and displays the best matches in the corpus for
said search query in order of relevance. The results display the keyword in context,
the relevance score of the match, the title of the movie, the year of publishing and the genre of the movie.</p>
<p>This is our final project for the course "Building NLP Applications (2022)" (KIK-LG211) at th University of Helsinki.</p>

## Built Using

* Flask
* Python 3
* HTML


## Installation and how to run the project

### Installing flask

First, create a project directory:

```
mkdir final_project
cd final_project
```

Install flask:

```
pip install Flask
```

### Cloning repository

In `final_project` directory clone `plague-inc` git repository and move to `plague-inc` directory 

```
git clone https://github.com/msainio/plague-inc
cd plague-inc
```

### Running Flask

First, move to directory `plague_project`:

```
cd plague_project
```

To run flask, set the following environment variables (also found in file `flask_vars`):

```
export FLASK_APP=plague_engine.py
export FLASK_ENV=development
export FLASK_RUN_PORT=8000
``` 

On Windows command line:

```
set FLASK_APP=plague_engine.py
set FLASK_ENV=development
set FLASK_RUN_PORT=8000
```

On Windows PowerShell:

```
$env:FLASK_APP = "plague_engine.py"
$env:FLASK_ENV = "development"
$env:FLASK_RUN_PORT = "8000"
```

Run Flask:

```
flask run
```

Lastly, copypaste `http://...` from the line beginning with `* Running on` and add `search` after the last forward slash.
 
## Usage

## Contributors

* Ines Fröjdö (https://github.com/ifrojdo)
* Aava Latokartano (https://github.com/alatokartano)
* Annika Rantala (https://github.com/annikarantala)
* Mitja Sainio (https://github.com/msainio)

## License

[MIT](https://en.wikipedia.org/wiki/MIT_License)

## Resources found helpful

* [Flask Example](https://github.com/miau1/flask-example/blob/master/README.md)
* [HTML Tutorial](https://www.w3schools.com/html/)
* [A Beginners Guide to writing a Kickass README](https://meakaakka.medium.com/a-beginners-guide-to-writing-a-kickass-readme-7ac01da88ab3)
* [How to Write a Good README File for Your GitHub Project](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/blob/master/README.md)

