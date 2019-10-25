import React from "react";
import { connect } from 'react-redux';

import Sentence from "./Sentence";
import EditSentence from "./EditSentence";
import { editField } from "../actions";

/**
 * Connected component for a Sentence, which can be in edit mode.
 * The editing prop determines the mode, and is passed in from the parent charge.
 * Props which are properties of the sentence are passed to a child
 * presentational component, which is either Sentence or EditSentence.
 * These components also receive a dispatching function, which is used by the
 * EditSentence component to send changes to the redux store.
 */
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
    return state.crecord.sentences[ownProps.sentenceId];
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