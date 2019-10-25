import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addAttorney } from "../actions";

/**
 * Component for adding a Attorney to a CRecord.
 * It starts with a textbox to enter the docket number of the attorney,
 * and a button.  Once the button is clicked, a attorney with that docket number
 * is added to the redux state. The new attorney will then be at the bottom of the list of attorneys, in edit mode,
 * so that the user can enter its data.
 */
function AddAttorney(props) {
    const { adder } = props;
    const [fullName, setFullName] = useState("");

    const handleChange = event => {
        setFullName(event.target.value);
    }

    const handleClick = () => {
        adder(fullName);
        setFullName("");
    }

    const handleKeyDown = event => {
        if (event.keyCode === 13) {
            event.preventDefault();
            event.stopPropagation();
            handleClick();
        }
    }

    return (
        <div className="addAttorney" >
           <span style={{marginLeft: "20px"}}>Full Name: </span>
           <input type="text" value={fullName} onChange={handleChange} onKeyDown={handleKeyDown}/>
           <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>Add Attorney</button>
        </div>
    );
}

function mapDispatchToProps(dispatch) {
    return { adder: fullName => {
            dispatch(addAttorney(fullName));
        }
    };
};

AddAttorney.propTypes = {
    /**
     * The callback which adds the attorney to state.
     */
    adder: PropTypes.func.isRequired
}

const AddAttorneyWrapper = connect(null, mapDispatchToProps)(AddAttorney);
export default AddAttorneyWrapper;