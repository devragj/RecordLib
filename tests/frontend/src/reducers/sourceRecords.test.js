import sourceRecordsReducer, { initialState } from "frontend/src/reducers/sourceRecords"
import { upsertSourceRecords } from "frontend/src/actions/sourceRecords"

// Example data returned by api /record/upload 
// 
const sourceRecordsResponseData = {
    "source_records": [
        {
            "id": "0e88f23d-9288-48ad-8a4c-38fe64d76ada",
            "caption": "",
            "docket_num": "",
            "court": "CP",
            "url": "",
            "record_type": "SUMMARY_PDF",
            "fetch_status": "FETCHED",
            "file": "CP-36-CR-0000434-2017_summary.pdf"
        }
    ]
}

describe('SourceRecordReducer', () => {
    it('adds a new source record to the state', () => {
        const action = upsertSourceRecords(sourceRecordsResponseData)
        const newState = sourceRecordsReducer(initialState, action)
        expect(newState).toEqual({
            allIds: [sourceRecordsResponseData.source_records[0].id],
            allSourceRecords: {
                [sourceRecordsResponseData.source_records[0].id]: sourceRecordsResponseData.source_records[0]
            }
        })
    })
})