# RecordLib

Library for handling Criminal Records information in Pennsylvania.

Right now this is only an experimental project for trying out some ideas and new tooling.




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
