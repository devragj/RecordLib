/** Display an Analysis of a CRecord, and provide a button to navigate to downloading petitions. 
 * 
 */
import React from "react"
import { connect } from "react-redux"
import Container from "@material-ui/core/Container"
import Button from "@material-ui/core/Button"

import { getPetitions } from "../actions"

function Analysis(props) {
    const { analysis, getPetitions } = props

    console.log("Analysis:")
    console.log(analysis)

    const petitions = analysis.decisions.map((d) => {
        return d.value
    }).flat()

    const submitForm = (e) => {
        e.preventDefault()
        console.log("submitting petitions")
        getPetitions(petitions)
    }

    return (
        <Container>
            <h2> Analysis </h2>
            <form onSubmit={submitForm}>
                <Button type="submit"> 
                   Get Petitions
               </Button>
            </form>
           
        </Container>
    )
}


function mapStateToProps(state) {
    return {analysis: state.analysis}
}

function mapDispatchToProps(dispatch) {
    return {getPetitions: (petitions) => dispatch(getPetitions(petitions))}
}

export default connect(mapStateToProps, mapDispatchToProps)(Analysis)