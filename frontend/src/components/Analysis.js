/** Display an Analysis of a CRecord, and provide a button to navigate to downloading petitions. 
 * 
 */
import React from "react"
import { connect } from "react-redux"
import Container from "@material-ui/core/Container"
import Button from "@material-ui/core/Button"
import PetitionDecision from "./PetitionDecision"
import { getPetitions } from "../actions"

function Analysis(props) {
    const { analysis, activeStepIndex, setActiveStepIndex} = props

    console.log("Analysis:")
    console.log(analysis)

    const petitions = analysis.decisions ? 
        analysis.decisions.map((d) => {
            return d.value
        }).flat() :
        []

    const submitForm = (e) => {
        e.preventDefault()
        setActiveStepIndex(activeStepIndex + 1)
    }

    return (
        <Container>
            <h2> Analysis </h2>
            { 
                analysis.decisions ? 
                    <form onSubmit={submitForm}>
                        <Button type="submit"> Get Petitions </Button>
                        {analysis.decisions.map((decision, idx) => {
                            return(<PetitionDecision key={idx} decision={decision}/>)
                        })}
                    </form> :
                    <p> You should submit the record for analysis first. </p>
            }
        </Container>
    )
}


function mapStateToProps(state) {
    if(state.analysis.analysis) {
        return {analysis: state.analysis.analysis}
    }
    return {analysis: {}}
}


export default connect(mapStateToProps)(Analysis)