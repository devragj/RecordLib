import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCase } from "../actions";
import EditCase from "./EditCase";

function AddCase(props) {
    const adder = props.adder;
    const [adding, setAdding] = useState(false);
    const [docketNumber, setDocketNumber] = useState("");

    const handleChange = event => setDocketNumber(event.target.value);
    const handleClick = () => {
        if (!adding) {
            adder(docketNumber);
        } else {
            setDocketNumber("");
        }

        setAdding(!adding);
    }

    return (
        <div className="addCase" >
           <span style={{marginLeft: "20px"}}>Docket Number: </span>
           <input type="text" value={docketNumber} onChange={handleChange} readOnly={adding}/>
           <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>{adding? "Done Adding Case": "Add Case"}</button>
           { adding && <EditCase caseId={docketNumber}/> }
        </div>
    );
}

function mapDispatchToProps(dispatch) {
    return { adder: docketNumber => {
            dispatch(addCase(docketNumber));
        }
    };
};

AddCase.propTypes = {
    /**
     * The callback which adds the case to state.
     */
    adder: PropTypes.func.isRequired
}

const AddCaseWrapper = connect(null, mapDispatchToProps)(AddCase);
export default AddCaseWrapper;