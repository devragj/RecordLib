# RecordLib

Library for handling Criminal Records information in Pennsylvania.

Right now this is only an experimental project for trying out some ideas and new tooling (e.g., trying out some of the newer python features like type annotations and data classes)




## Goals

The ultimate goal is to develop a flexible and transparent pipeline for analyzing criminal records in Pennsylvania for expungeable and sealable cases and charges. We'd like to be able to take various inputs - pdf dockets, web forms, scanned summary sheets - build an idea of what a person's criminal record looks like, and then produce an analysis of what can be expunged or sealed (and _why_ we think different things can be expunged or sealed).


The pieces of this pipeline could be used in different interfaces.

A commandline tool could process a list of documents or the names of clients, and try to analyze the whole list in bulk.

A web application could take a user through the steps of the pipeline and allow the user to see how the analysis proceeds from inputs to output petitions. The application could allow the user to load some documents, then manually check the Record that the system builds out of those documents before proceeding to analyze the record.

Ideally, the expungement rules that get applied will also be written in a clear enough way that non-programmer lawyers can review them.

## Domain Model

There are I think five kinds of objects involved in this framework.

1. Criminal Records raw inputs - these are things like a pdf of a docket or a web form that asks a user about criminal record information.
2. A Criminal Record - the authoritative representation of what a person's criminal record is. Its made by compiling raw inputs.
3. Expungement/Sealing Rules - functions that take a Record and return an analysis of how a specific expungement or sealing rule applies to the record. What charges or cases does a specific rule allow to be sealed/expunged?
4. Analysis - some sort of object that encapsulates how different rules apply to a record
5. Document Generator - a function that takes an analysis and information about a user (i.e., their attorney identification info) and produces a set of documents that includes drafts of petitions for a court.


## Usage

### download_docs

`download_docs` is a cli that can collect summary sheets or dockets for testing purposes. It relies on having the DocketScraperAPI application running.

See the script's help information for details.

```
me: download_docs --help
Usage: download_docs [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  docket-numbers  Download dockets or summary sheets for the docket numbers...
  names           Download dockets from a list of names.
  random          Download <n> random "summary" documents or "docket"...
```

### analyze

`analyze` is a cli for reviewing a record for expungements and sealings. Currently, you can pass it a single summary sheet. It will build a criminal record out of the summary sheet and then return a json object that reports what expungements and sealings the record may be eligible for.

```
me: analyze --help
Usage: analyze [OPTIONS]

Options:
  -ps, --pdf-summary PATH    [required]
  -td, --tempdir PATH
  -rc, --redis-collect TEXT  connection to redis, in the form
                             [host]:[port]:[db number]:[environment name]. For
                             example, 'localhost:6379:0:development'
  --help                     Show this message and exit.
```

### expunge

`expunge` is a cli for generating petitions. It has subcommands. 

```
me: expunge --help
Usage: expunge [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dir
```

`expunge dir` will generate petitions for all the summary and docket pdf files in finds in the target directory. This command only makes sense to run when all the files
in the target directory relate to one person. 

```
me: expunge dir --help
Usage: expunge dir [OPTIONS]

Options:
  -d, --directory PATH            [required]
  -a, --archive PATH              [required]
  -et, --expungement-template PATH
                                  [required]
  -st, --sealing-template PATH    [required]
  --atty-name TEXT
  --atty-org TEXT
  --atty-org-addr TEXT
  --atty-org-phone TEXT
  --atty-bar-id TEXT
  -td, --tempdir PATH
  --help                          Show this message and exit.

```

For example, this command creates an archive of petions generated from processing all the files in the `tests/data/summaries` directory. 

```
expunge dir --directory tests/data/summaries/ --archive expungements.zip -et tests/templates/790ExpungementTemplate_usingpythonvars.docx -st tests/templates/791SealingTemplate.docx 
```

## Developing

The whole project lives in a single repository, but it has three pieces:

1. The legal logic in `RecordLib/`
2. A Django web api in `backend/`
3. A Reach frontend in `frontend/`

To start developing, clone the repository and install dependencies from the root directory with `pipenv install`.

### Legal logic

The `RecordLib` directory contains modules for parsing and analyzing records. 

#### Setup

`RecordLib` also depends on the utility pdftotext. This utility is included in
most Linux distributions.  For other operating systems, find it here: 
http://www.xpdfreader.com/download.html.  Download the command line tools and 
place pdftotext somewhere in your PATH.



**MYSQL**

The library also recommends that you set up a database of mappings from statutes to offense grades.
RecordLib needs to be able to guess the grade of an offense, when the grade is not recorded. The project
currently uses the same implementation as the ExpungementGenerator. There is a mysql database (sql dump is here: https://github.com/NateV/Expungement-Generator/blob/master/Expungement-Generator/migrations/2%20-%20cpcms_aopc_summary.sql) 

Set up a mysql database and import this dump file `mysql -u username -p database_name < file.sql`.

Then set up a `.env` file in the root directory of the project with the variables:

```
mysql_host=localhost
mysql_user=myuser
mysql_pw=WhateverYourPasswordIs
SECRET_KEY='super-duper-secret-Gs'
DEBUG=TRUE

PSQL_USER=myname
PSQL_PW=mypass
PSQL_HOST=127.0.0.1
PSQL_NAME=recordlibdb
STATIC_ROOT=static/

```

Reload your virtual environment with `exit` and `pipenv shell`. You can confirm if the database is working with `pytest tests/test_getgrade.py`. If the database connection fails, you'll see a Error in the test's output and the tests will fail. 

#### Testing

Run automated tests with `pytest`.

Grammars need to be tested on lots of different documents. The tests include tests that will try to parse all the dockets in a folder `tests/data/[summaries|dockets]`. If you want those tests to be meaningful, you need to put dockets there.

You could do this manually by downloading dockets and saving them there. You can also use a helper script that randomly generates docket numbers and then uses [natev/DocketScraperAPI](https://hub.docker.com/r/natev/docketscraper_api) to download those dockets. To do this

1. download and run the DocketScraperAPI image with `docker run -p 5000:8800 natev/docketscraper_api`
2. in this project environment, run `download (summaries | dockets) [-n = 1]`



### Django backend 

The backend requires the command-line utility pdftotext.  This utility is included in
most Linux distributions.  For other operating systems, find it here: 
http://www.xpdfreader.com/download.html.  Download the command line tools and 
place pdftotext somewhere in your PATH.

**POSTGRES**. The django app uses a postgres backend. You can set up a local database and configure
the variables listed below.


Initial setup:
For the backend, create a directory named `tmp` 
inside the directory `backend/cleanslate`.
For the frontend, run `yarn install` within the directory `frontend`.

To run the app, first start the Django REST backend.
To start the backend, in the outer RecordLib directory,
type `pipenv shell`.
Then `cd backend` and then `python manage.py runserver`.


### React App frontend

Next, start the frontend.
To do this, open a new terminal window
and navigate to  the `frontend` directory. 
Then type `yarn start`. 

Currently, you can upload a Summary PDF.
The app will display information from the `CRecord`
generated from the Summary.


## Development Docker Deployment

You can use docker-compose to set up a whole development deployment of the site, and code changes will 
reload live (with one caveat).

Just run `docker-compose -f deployment/docker-compose-dev.yml build` and then `up`. 

To get the frontend rebuilding, you still need to run `yarn run watch` in a separate terminal. 

## Aspirational Example Usage

	person = Person(first_name="Joan", last_name="Smith", date_of_birth=date(1970, 1, 1))
    record = CRecord(person)
    assert record.cases == [] # True

    docket = Docket("path/to/docket.pdf")
    summary = Summary("path/to/summary.pdf")

    record.add_docket(docket)
    record.add_summary(summary)

    # CRecord loaded all the cases from the docket and summary
    assert len(record.cases) > 0

	record.cases == [a list of cases]
	record.cases[0].charges == [a list of charges on a case]
	record.cases[0].feescosts = (amt owed: ..., amt paid: ..., fees that could be waived.)

    analysis_container = (
        Analysis(record)
	.rule(expunge_deceased)
	.rule(expunge_over70_years)
	.rule(expunge_nonconvictions)
	.rule(seal_convictions)
    )

    remaining_charges = analysis_container.remaining_recordord
    analysis = analysis_container.analysis

	analysis ==
	{
		personInfo: {},
		full_expungments: [case],
		partial_expungements: [case],
		sealing: [
			{case: []
			 	charges: []
			}
		]

	}

    attorney_info = Attorney(name="Jane Smith", organization="Legal Services Org of X County", barid="xxxxxx")

    success_or_fail = generate_petiton_packet(original_record, analysis, attorney_info)
    print(success_or_fail)


## Roadmap

Right now I'm working on several pieces more or less simultaneously.

1. grammars for parsing summary sheets and dockets from pdfs
2. The CRecord class for managing information about a person's record (what methods and properties does it need to have?)
3. RuleDef functions - functions that take a CRecord and apply a single legal rule to it. I'm trying to figure out the right thing to return.





## Developing Grammars

The project currently uses `parsimonious` and Parsing Expression Grammars to parse pdf documents and transform them from a pdf file to an xml document.

Developing grammars is pretty laborious. Some tips:

**Parse text w/ subrule** With parsimonious, you can try parsing a bit of text with a specific rule, with `mygrammar['rule'].parse("text")`

So if you have a variable of the lines of your document, then you can more quickly test specific parts of the doc with specific parts of the grammar.

**Autogenerate the NodeVisitor** RecordLib with Parsimonious transforms a document with a grammar in two phases. First, Parsimonious uses a grammar to build a tree of the document. Then a NodeVisitor visits each node of the tree and does something, using a NodeVisitor subclass we have to create. The `CustomVisitorFactory` from RecordLib creates such a NodeVisitor with default behavior that's helpful to us. By passing the Factory a list of the terminal and nonterminal symbols in the grammar, the Factory will give us a class that will take a parsed document and wrap everything under terminal and nonterminal symbols in tags with the symbol's name. Terminal symbols will also have their text contents included as the tag content. NonTerminal symbols will only wrap their children (who are eventually terminal symbols).

## other issues

**Text from PDFs**
Right now pdf-to-text parsing is done with pdftotext. I think it works really well, but relying on a binary like that does limit options for how to deploy a project like this (i.e, couldn't use heroku, I think). It also requires writing a file temporarily to disk, which is kind of yucky. The best-known python pdf parser, PyPDF2, appears not be maintained anymore.

**Handing uncertainty**
Its important that an Analysis be able to say that how a rule applies to a case or charge is uncertain. For example, if the grade is missing from a charge, the answer to expungement questions isn't True or False, its "we don't know because ..."  

## Additional Notes

Statutes contain a lot of section symbols: §. To make this symbol using vim or vim inspired keybindings, use CTL-K SE. That's Control K, then the uppercase letters S and E.