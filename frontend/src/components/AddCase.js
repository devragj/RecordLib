import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCase } from "../actions";
import EditCase from "./EditCase";

/**
 * Component for adding a Case to a CRecord.
 * It starts with a textbox to enter the docket number of the case,
 * and a button.  Once the button is clicked, a case with that docket number
 * is added to the redux state.  The component then displays the EditCase
 * component, to enter the case information.  Clicking the button (whose label
 * has changed) again will hide the EditCase component.
 */
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