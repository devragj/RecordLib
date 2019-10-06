import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCase } from "../actions";

/**
 * Component for adding a Case to a CRecord.
 * It starts with a textbox to enter the docket number of the case,
 * and a button.  Once the button is clicked, a case with that docket number
 * is added to the redux state. The new case will then be at the bottom of the list of cases, in edit mode,
 * so that the user can enter its data.
 */
function AddCase(props) {
    const { adder } = props;
    const [docketNumber, setDocketNumber] = useState("");

    const handleChange = event => setDocketNumber(event.target.value);
    const handleClick = () => {
        adder(docketNumber);
        setDocketNumber("");
    }

    return (
        <div className="addCase" >
           <span style={{marginLeft: "20px"}}>Docket Number: </span>
           <input type="text" value={docketNumber} onChange={handleChange} />
           <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>Add Case</button>
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