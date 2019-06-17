# RecordLib

Library for handling Criminal Records information in Pennsylvania.

Right now this is only an experimental project for trying out some ideas and new tooling (e.g., trying out some of the newer python features like type annotations and data classes)

## Aspirational Usage

	try:
		record = Record({a dict of a person's criminal record}
	except RecordError
		print("Record not valid because: " + RecordError)

	record.person.name = "info about a person the record relates to"
	record.cases = [a list of cases]
	record.cases[0].charges = [a list of charges on a case]
	record.cases[0].feescosts = (amt owed: ..., amt paid: ..., fees that could be waived.)

	analysis = record.analyze()
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

### idempotent combining

I think we might want kind of algebra of Records. Like you can take a docket, parse it to a Record, and take a Summary and parse that to a record. Then add those two Records together, and the addition function should combine the two records intelligently - fail if the "person" is not the same, and combine cases without duplicating, combine charges without duplicating.

	rec1 = from_pdf(case_docket)
	rec2 = from_pdf(summary)

	full_rec = rec1 + rec2

Alternatively, it might be better to have idempotent but more explicit methods:

	rec = CRecord()
	docket = Docket("case_docket.pdf")
	summary = Summary("summary.pdf")
	rec.add_docket(docket)
	rec.add_summary(summary)

## Testing

Run automated tests with `pytest`.

Grammars need to be tested on lots of different documents. The tests include tests that will try to parse all the dockets in a folder `tests/data/[summaries|dockets]`. If you want those tests to be meaningful, you need to put dockets there.

You could do this manually by downloading dockets and saving them there. You can also use a helper script that randomly generates docket numbers and then uses [natev/DocketScraperAPI](https://hub.docker.com/r/natev/docketscraper_api) to download those dockets. To do this

1. download and run the DocketScraperAPI image with `docker run natev/DocketScraperAPI -p 8800:8800`
2. in this project environment, run `download (summaries | dockets) [-n = 1]`

TODO I would like to try out `hypothesis` for property-based testing.


## other issues

Right now pdf-to-text parsing is done with PyPDF2. That seeems to be unmaintained. We might do the command line pdftotext binary, or maybe there's some other python library we could use? Maybe parse_pdf should use dependency injection to be able to swap out text-extractors.
