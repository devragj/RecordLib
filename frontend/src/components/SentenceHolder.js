import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Sentence from "./Sentence";
import EditSentence from "./EditSentence";
import { editField } from "../actions";


function SentenceHolder(props) {
    return (
        <div className="sentenceHolder" >
            { !props.editing?
                <Sentence {...props} />
                : <EditSentence {...props} />
            }
        </div>
    );
};

function mapStateToProps(state, ownProps) {
    return state.entities.sentences[ownProps.sentenceId];
};

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Sentence
 * object being edited.  It is used by the EditSentence component.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return {
        modifier: (key, value) => {
            dispatch(editField('sentences', ownProps.sentenceId, key, value))
        }
    };
};

const SentenceHolderWrapper = connect(mapStateToProps, mapDispatchToProps)(SentenceHolder);
export default SentenceHolderWrapper;