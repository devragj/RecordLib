import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addSentence } from "../actions";

/**
 * Component for adding a Sentence to a Charge.
 * It displays a button.  Once the button is clicked, a new sentence is added to the redux state.
 * The new sentence will then be at the bottom of the list of sentences for this charge, where the user can
 * enter its data.
 */
function AddSentence(props) {
    const { adder } = props;

    const handleClick = () => {
        adder();
    }

    return (
        <div className="addSentence" style={{marginTop: "15px", marginBottom: "10px"}}>
            <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>Add Sentence</button>
        </div>
    );
}

AddSentence.propTypes = {
    adder: PropTypes.func.isRequired
}

function mapDispatchToProps(dispatch, ownProps) {
    return { adder: () => {
            dispatch(addSentence(ownProps.chargeId));
        }
    };
};

const AddSentenceWrapper = connect(null, mapDispatchToProps)(AddSentence);
export default AddSentenceWrapper;