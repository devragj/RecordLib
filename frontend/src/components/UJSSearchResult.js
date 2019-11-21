import React, { useState } from "react"
import { connect } from "react-redux"
import CircularProgress from "@material-ui/core/CircularProgress"
import Typography from "@material-ui/core/Typography"
import Link from "@material-ui/core/Link"
import Checkbox from "@material-ui/core/Checkbox"
import Grid from "@material-ui/core/Grid"

import {  toggleSelectedUJSSearchCases } from "../actions/ujs"

function DocketItem(props) {
    /**
     * 
     * n.b. removed otn to save space.
     */
    const {
        court, caption, case_status, dob, docket_number, 
        docket_sheet_url, summary_url, useLinks, 
        docketSelected, summarySelected,
        docketChangeHandler, summaryChangeHandler,
    } = props
    return(
        <Grid container direction="row" justify="center" alignItems="center">
            <Grid item xs={1}>{court}</Grid>
            <Grid item xs={2}>{docket_number}</Grid>
            <Grid item xs={2}>{caption}</Grid>
            <Grid item xs={1}>{case_status}</Grid>
            <Grid item xs={1}>{dob}</Grid>
            <Grid item xs={1}>
                {useLinks ? 
                    <Link href={docket_sheet_url} rel="noreferrer" target="_blank">D</Link> :
                    docket_sheet_url
                }
            </Grid>
            <Grid item xs={1}>
                <Checkbox 
                    onChange={docketChangeHandler}
                    checked={docketSelected}
                    color="default"
                />
            </Grid>
            <Grid item xs={1}>
                {useLinks ? 
                    <Link href={summary_url} rel="noreferrer" target="_blank">S</Link> :
                    summary_url
                }
            </Grid>
            <Grid item xs={1}>
                <Checkbox
                    checked={summarySelected}
                    onChange={summaryChangeHandler}
                    color="default"
                />
            </Grid>
        </Grid>
 
    )
}

function UJSSearchResults(props) {
    /**
     * Component rendered when there are ujs search results to display.
     * 
     * Renders a table of search results. 
     */
    const { casesFound, toggleSelected } = props
    
    const [allDocketsSelected, setAllDocketsSelected] = useState(true)    
    const [allSummariesSelected, setAllSummariesSelected] = useState(false)


    const toggleAllDockets = () => {
        /**
         * toggling the All Dockets checkbox, and changing the values of all the 
         * checkboxes. Only change the state at the end, and use the current state here,
         * because setState is async and doesn't take effect right away
         */
        if (allDocketsSelected) {
            casesFound.result.forEach(docketNum => {
                toggleSelected("docket", docketNum, false)                
            }) 
        } else {
            casesFound.result.forEach(docketNum => {
                toggleSelected("docket", docketNum, true)
            })
        }
        setAllDocketsSelected( !allDocketsSelected )
    }
    
    const toggleAllSummaries = () => {
        if (allSummariesSelected) {
            casesFound.result.forEach(docketNum => {
                toggleSelected("summary", docketNum, false)                
            }) 
        } else {
            casesFound.result.forEach(docketNum => {
                toggleSelected("summary", docketNum, true)
            })
        }
        setAllSummariesSelected( !allSummariesSelected )
    }


    const makeChangeHandler = (documentType, doc_num) => {
        /**
         * documentType is either summary or docket
         * doc_num is the number of the case, i.e. CP-1234
         */
        return(
            () => {
                toggleSelected(documentType, doc_num)
            }
        )
    }

    return(
        <React.Fragment >
            <Grid item xs={12}>
                <Typography variant="h6">Search Results</Typography>
            </Grid>
            <DocketItem 
                court={"COURT"}
                docket_number={"DOCKET NUMBER"}
                caption={"CAPTION"}
                case_status={"CASE STATUS"}
                dob={"DATE OF BIRTH"}
                otn={"OTN"}
                docket_sheet_url={"DOCKET"}
                docketSelected={allDocketsSelected}
                docketChangeHandler={toggleAllDockets}
                summarySelected={allSummariesSelected}
                summaryChangeHandler={toggleAllSummaries} 
                summary_url={"SUMMARY"}
                />
            {
                casesFound.result.length === 0 ?
                    <Grid item> 
                        <Typography variant="body1"> 
                            No dockets found
                        </Typography>
                    </Grid> :
                    <React.Fragment>
                        {
                            casesFound.result.map((doc_num) => {
                                return(
                                    <DocketItem key={doc_num} 
                                        useLinks={true} 
                                        court={"MDJ"} 
                                        docketChangeHandler={makeChangeHandler("docket", doc_num)}
                                        summaryChangeHandler={makeChangeHandler("summary", doc_num)}
                                        {...casesFound.entities[doc_num]}/>
                                )
                            }) 
                        }
                    </React.Fragment>
            }
        </React.Fragment>
    )
}

function mapDispatchToProps(dispatch) {
    /** mapDispatchToProps for wrapping the UJSSearchResultsWrapper
     * 
     */
    return {
        toggleSelected: (docType, doc_num, newValue) => dispatch(
            toggleSelectedUJSSearchCases(docType, doc_num, newValue))
    }
}

const UJSSearchResultsWrapper = connect(null, mapDispatchToProps)(UJSSearchResults)

function UJSSearchResultsContainer(props) {
    /**
     * Component shows UJS search results, or shows if the search is still processing.
     */
    switch(props.results.status) {
        case(null):
            return (<p>No search yet</p>)
        case("Started"):
            return (
                <Grid item xs={2}>
                    <CircularProgress/>
                </Grid>
            )
        case("Success"):
            return(
                <UJSSearchResultsWrapper {...props.results}/>
            )
       default:
            return (
                <Grid item xs={8}>
                    <Typography variant="body1">
                         Uh oh. Something went wrong. You can try again, or search for dockets manually
                         <Link href="https://ujsportal.pacourts.us/"> here.</Link> 
                         Contact your site administrator to let them know about the error.
                    </Typography>
                </Grid>
            )
    }
}

export default UJSSearchResultsContainer