import React from "react"
import { connect } from "react-redux"
import CRecordWrapper from "./CRecord"
import Container from "@material-ui/core/Container"
import FormGroup from "@material-ui/core/FormGroup"
import Button from "@material-ui/core/Button"
import { analyzeCRecord } from "../actions/crecord"


function RecordEdit(props) {
    const { crecordFetched, analyzeCRecord } = props 
   
    const submitHandler = (e) => { 
        e.preventDefault()
        analyzeCRecord()
    }

    return (
        <Container>
            <form onSubmit={submitHandler}>
                <FormGroup> 
                    <Button type="submit"> Analyze </Button>
                </FormGroup>
            </form>
            {crecordFetched? <CRecordWrapper/> : <p> No Record yet (process for making a new record will go here) </p>}
        </Container>
    )
}

function mapStateToProps(state) {
    return {crecordFetched: state.crecord? true: false}
}

function mapDispatchToProps(dispatch) {
    return {analyzeCRecord: () => {
        dispatch(analyzeCRecord()) 
    }}
}

export default connect(mapStateToProps, mapDispatchToProps)(RecordEdit)
