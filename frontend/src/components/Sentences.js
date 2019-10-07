import React from "react";
import PropTypes from 'prop-types';

import SentenceHolderWrapper from "./SentenceHolder";
import AddSentenceWrapper from "./AddSentence";
import ShowHideList from "./ShowHideList";


function Sentences(props) {
    const sentencesStyle = {gridColumn: "1 / 3"};
    const { sentences, chargeId, editing } = props;
    const sentencesRendered = sentences.map(sentenceId => {
            return <SentenceHolderWrapper key={sentenceId} sentenceId={sentenceId} editing={editing}/>
        }
    );

    if (editing) {
        const addSentenceKey = chargeId + 'addSentence';
        const addSentence = <AddSentenceWrapper chargeId={chargeId} key={addSentenceKey}/>
        sentencesRendered.push(addSentence);
    };

    return (
        <div className="sentences" style={sentencesStyle}>
        {sentencesRendered.length > 0 &&
           <ShowHideList hidden={!editing} title="Sentences" list={sentencesRendered} />
        }
        </div>
    );
}

Sentences.propTypes = {
    /**
        The list of sentence ids.
    */
    sentences: PropTypes.array.isRequired,
    /**
        The id of the charge containing the sentences.
    */
    chargeId: PropTypes.string.isRequired,
    /**
        This component wil be used either in the Case component,
        in which case editing is false, or in the EditCase
        component, in which case editing is true.
    */
    editing: PropTypes.bool
}

export default Sentences;