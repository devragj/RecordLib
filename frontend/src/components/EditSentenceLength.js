import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { editSentenceLength } from "../actions";

function EditSentenceLength(props) {
    const { sentence_length, modifier } = props;
    const sentenceLengthStyle = { gridColumn: "1 / 3",  margin: '15px',
        border: '1px solid black', borderRadius: '5px', padding: '10px', width: '370px', textAlign: 'center' };

    const getPropertyModifier = key => {
        return event => modifier(key, event.target.value);
    }

    return (
        <div className="editSentenceLength" style={sentenceLengthStyle}>
             <div style={{ textAlign: 'center' }}> Sentence Length </div>
             <div className="editLength">
                 Min Time:  <input type="text" value={sentence_length.min_time} onChange={getPropertyModifier('min_time')}/> days
             </div>
             <div className="editLength">
                 MaxTime:  <input type="text" value={sentence_length.max_time} onChange={getPropertyModifier('max_time')}/> days
             </div>
        </div>
    );
}

EditSentenceLength.propTypes = {
    sentenceId: PropTypes.string,
    sentence_length: PropTypes.shape({
        min_time: PropTypes.string,
        max_time: PropTypes.string
    }),
    modifier: PropTypes.func
}

function mapStateToProps(state, ownProps) {
    return { sentence_length: state.entities.sentences[ownProps.sentenceId].sentence_length };
};

function mapDispatchToProps(dispatch, ownProps) {
    return { modifier: (key, value) => {
            dispatch(editSentenceLength(ownProps.sentenceId, key, value))
        }
    };
};

const EditSentenceLengthWrapper = connect(mapStateToProps, mapDispatchToProps)(EditSentenceLength);
export default EditSentenceLengthWrapper;