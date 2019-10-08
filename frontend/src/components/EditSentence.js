import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import EditField from "./EditField";
import { editField } from "../actions";
import EditSentenceLengthWrapper from "./EditSentenceLength";

/**
 * Component to edit a sentence, including supplying values to a newly-created sentence.
 */
function EditSentence(props) {
    const { id, sentence_date, sentence_type, sentence_period, modifier } = props;
    const sentenceStyle = { display: 'grid', gridTemplateColumns: '200px 270px 270px', margin: '15px',
        border: '1px solid black', borderRadius: '5px', padding: '10px', width: '760px'};

    /**
     * This function starts with the modifier function, which expects a key,value pair
     * and returns a function which takes a key and returns a function which expects a value.
     */
    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }

    return (
        <div className="editSentence" id={id} style={sentenceStyle}>
            <EditField item={sentence_date} label="Date: " modifier={getPropertyModifier('sentence_date')} />
            <EditField item={sentence_type} label="Type: " modifier={getPropertyModifier('sentence_type')} />
            <EditField item={sentence_period} label="Period: " modifier={getPropertyModifier('sentence_period')} />
            <EditSentenceLengthWrapper sentenceId={id} />
        </div>
    );
}

EditSentence.propTypes = {
    id: PropTypes.string,
    sentence_date: PropTypes.string,
    sentence_type: PropTypes.string,
    sentence_period: PropTypes.string,
    modifier: PropTypes.func
}

function mapStateToProps(state, ownProps) {
    return state.crecord.entities.sentences[ownProps.sentenceId];
};

/**
 * This function returns a function which take a key,value pair
 * and associates the value with that key in the Sentence
 * object being edited.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: (key, value) => {
            dispatch(editField('sentences', ownProps.sentenceId, key, value))
        }
    };
};

const EditSentenceWrapper = connect(mapStateToProps, mapDispatchToProps)(EditSentence);
export default EditSentenceWrapper;