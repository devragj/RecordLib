import React from "react"
import { connect } from "react-redux"
import Button from "@material-ui/core/Button"
import Grid from "@material-ui/core/Grid"
import { searchUJSByName, uploadUJSDocs } from "../actions/ujs"

import UJSSearchResultsContainer from "./UJSSearchResult"


function NameSearch(props) {
    const { applicant, ujsSearchResults, searchUJSByName, uploadUJSDocs } = props
    const missingSearchFields = applicant.first_name === "" || applicant.last_name === ""

    const searchClickHandler = () => {
        searchUJSByName(applicant)
    }

    const uploadUJSDocsClickHandler = () => {
        console.log("uploading the selected cases to the server.")
        uploadUJSDocs()
    }

    const anySearchedCasesSelected = ujsSearchResults.casesFound.result.length > 0
    return(
        <div>
            <Grid container direction="row" alignItems="center" alignContent="center" justify="space-around">
                <Grid item xs={3}>
                    <Button 
                        variant="contained" 
                        color="primary" 
                        disabled={missingSearchFields}
                        onClick={searchClickHandler}> Search ujs (optional and slow) </Button>
                </Grid>
                <Grid item xs={3}>
                    <Button 
                        variant="contained"
                        color="primary"
                        disabled={!anySearchedCasesSelected}
                        onClick={uploadUJSDocsClickHandler}> Process selected cases </Button>
                </Grid>
            </Grid>
            <Grid container direction="row" alignItems="center" alignContent="center" justify="space-around">
                {
                    <UJSSearchResultsContainer results={ujsSearchResults} />
                }
            </Grid>
        </div>
    )
}

function mapStateToProps(state) {
    return({
        applicant: state.applicantInfo.applicant,
        ujsSearchResults: state.ujsSearchResults,
        crecord: state.crecord,
    })
}

function mapDispatchToProps(dispatch, ownprops) {
    return {
        searchUJSByName: (applicant) => {
            return dispatch(searchUJSByName(applicant.first_name, applicant.last_name, applicant.date_of_birth));
        },
        uploadUJSDocs: () => {
            return dispatch(uploadUJSDocs())
        }
    }
}


const NameSearchWrapper = connect(mapStateToProps, mapDispatchToProps)(NameSearch)

export default NameSearchWrapper;