import applicantInfoReducer from "frontend/src/reducers/applicant"
import { ADD_OR_REPLACE_APPLICANT } from "frontend/src/actions/applicant"

describe('applicantReducer', () => {
    it('adds an initial applicant', () => {
        const newApplicant = {
            first_name: 'John',
            last_name: 'Smith',
            date_of_birth: "1950-10-01",
            date_of_death: "2010-10-01",
            ssn: 'abcd',
            address: '1234 Main St',
            aliases: ["Joey", "Smiley"],
        };
        const result = applicantInfoReducer(undefined, {type: ADD_OR_REPLACE_APPLICANT, payload: newApplicant}) 
        console.log(result)
        expect(result).toEqual({
            applicant: {
                first_name: 'John',
                last_name: 'Smith',
                date_of_birth: "1950-10-01",
                date_of_death: "2010-10-01",
                ssn: 'abcd',
                address: '1234 Main St',
                aliases: ["Joey", "Smiley"],
                editing: true,
            },
            aliases: {
                Joey: "Joey",
                Smiley: "Smiley"
            }
        })

    })

})