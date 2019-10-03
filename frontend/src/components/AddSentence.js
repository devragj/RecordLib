import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addSentence } from "../actions";
import EditSentenceWrapper from "./EditSentence";

function AddSentence(props) {
    const { adder, sentenceId } = props;
    const [adding, setAdding] = useState(false);

    const handleClick = () => {
        if (!adding) {
            adder();
        }

        setAdding(!adding);
    }

    return (
        <div className="addSentence" style={{marginTop: "15px", marginBottom: "10px"}}>
           <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>{adding? "Done Adding Sentence": "Add Sentence"}</button>
           { adding && <EditSentenceWrapper sentenceId={sentenceId}/> }
        </div>
    );
}

AddSentence.propTypes = {
    sentenceId: PropTypes.string.isRequired,
    /**
     * The callback which adds the sentence to state.
     */
    adder: PropTypes.func.isRequired
}

function mapStateToProps(state, ownProps) {
    const index = ownProps.nextIndex - 1;
    const sentenceId = ownProps.chargeId + 'sentences@' + index;
    return { sentenceId };
};

function mapDispatchToProps(dispatch, ownProps) {
    const index = ownProps.nextIndex;
    const sentenceId = ownProps.chargeId + 'sentences@' + index;
    return { adder: () => {
            dispatch(addSentence(sentenceId, ownProps.chargeId));
        }
    };
};

const AddSentenceWrapper = connect(mapStateToProps, mapDispatchToProps)(AddSentence);
export default AddSentenceWrapper;