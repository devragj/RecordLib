import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import EditField from "./EditField";
import { editField } from "../actions";

function EditSentence(props) {
    const { id, sentence_date, sentence_type, sentence_period, sentence_length, modifier } = props;
    const sentenceStyle = { display: 'grid', gridTemplateColumns: '200px 270px 270px', margin: '15px',
        border: '1px solid black', borderRadius: '5px', padding: '10px', width: '760px'};

    const getPropertyModifier = key => {
        return value => modifier(key, value);
    }

    return (
        <div className="editSentence" id={id} style={sentenceStyle}>
            <EditField item={sentence_date} label="Date: " modifier={getPropertyModifier('sentence_date')} />
            <EditField item={sentence_type} label="Type: " modifier={getPropertyModifier('sentence_type')} />
            <div></div>
            <EditField item={sentence_period} label="Period: " modifier={getPropertyModifier('sentence_period')} />
            <EditField item={sentence_length.min_time} label="Min Time: " modifier={getPropertyModifier('sentence_length.min_time')} />
            <EditField item={sentence_length.max_time} label="Max Time: " modifier={getPropertyModifier('sentence_length.max_time')} />
        </div>
    );
}

EditSentence.propTypes = {
    id: PropTypes.string,
    sentence_date: PropTypes.string,
    sentence_type: PropTypes.string,
    sentence_period: PropTypes.string,
    sentence_length: PropTypes.shape({
        min_time: PropTypes.number,
        max_time: PropTypes.number
    }),
    modifier: PropTypes.func
}

function mapStateToProps(state, ownProps) {
    return state.entities.sentences[ownProps.sentenceId];
};

function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: (key, value) => {
            dispatch(editField('sentences', ownProps.sentenceId, key, value))
        }
    };
};

const EditSentenceWrapper = connect(mapStateToProps, mapDispatchToProps)(EditSentence);
export default EditSentenceWrapper;